from flask import Flask, request, jsonify
from models import db, Product, Inventory, InventoryTransaction, Warehouse, Supplier, ProductSupplier
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stockflow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create DB
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return {
        "message": "StockFlow API is ONNN!!",
        "endpoints": [
            "/api/products",
            "/api/inventory/transaction",
            "/api/companies/<id>/alerts/low-stock"
        ]
    }

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json

    # Validate required fields
    required_fields = ['name', 'sku', 'price']
    for field in required_fields:
        if field not in data:
            return {"error": f"{field} is required"}, 400

    try:
        with db.session.begin():  # atomic transaction

            # Check SKU uniqueness
            existing = Product.query.filter_by(sku=data['sku']).first()
            if existing:
                return {"error": "SKU already exists"}, 409

            product = Product(
                name=data['name'],
                sku=data['sku'],
                price=Decimal(str(data['price'])),
                company_id=data.get('company_id')
            )

            db.session.add(product)
            db.session.flush()  # get ID without committing

        return {
            "message": "Product created",
            "product_id": product.id
        }, 201

    except IntegrityError:
        db.session.rollback()
        return {"error": "Database integrity error"}, 500

    except Exception:
        db.session.rollback()
        return {"error": "Unexpected error occurred"}, 500

@app.route('/api/inventory/transaction', methods=['POST'])
def update_inventory():
    data = request.json

    product_id = data['product_id']
    warehouse_id = data['warehouse_id']
    change = data['change']  # +10 or -5

    inventory = Inventory.query.filter_by(
        product_id=product_id,
        warehouse_id=warehouse_id
    ).first()

    if not inventory:
        inventory = Inventory(
            product_id=product_id,
            warehouse_id=warehouse_id,
            quantity=0
        )
        db.session.add(inventory)

    inventory.quantity += change

    txn = InventoryTransaction(
        product_id=product_id,
        warehouse_id=warehouse_id,
        change=change,
        type=data.get('type', 'adjustment')
    )

    db.session.add(txn)
    db.session.commit()

    return {"message": "Inventory updated"}


from models import ProductSupplier, Supplier, Warehouse

@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def low_stock(company_id):

    alerts = []
    recent_days = 30

    products = Product.query.filter_by(company_id=company_id).all()

    for product in products:

        # Get recent sales records
        sales_records = InventoryTransaction.query.filter(
            InventoryTransaction.product_id == product.id,
            InventoryTransaction.type == 'sale',
            InventoryTransaction.created_at >= datetime.utcnow() - timedelta(days=recent_days)
        ).all()

        if not sales_records:
            continue

        total_sales = sum(abs(txn.change) for txn in sales_records)
        avg_daily_sales = max(total_sales / recent_days, 1)

        inventories = Inventory.query.filter_by(product_id=product.id).all()

        # Get supplier (if exists)
        ps = ProductSupplier.query.filter_by(product_id=product.id).first()
        supplier_data = None

        if ps:
            supplier = Supplier.query.get(ps.supplier_id)
            if supplier:
                supplier_data = {
                    "id": supplier.id,
                    "name": supplier.name,
                    "contact_email": supplier.contact_email
                }

        for inv in inventories:

            # Use dynamic threshold if exists
            threshold = getattr(product, 'threshold', 20)

            if inv.quantity < threshold:

                # Avoid division issues
                days_left = int(inv.quantity / avg_daily_sales) if avg_daily_sales > 0 else None

                warehouse = Warehouse.query.get(inv.warehouse_id)

                alerts.append({
                    "product_id": product.id,
                    "product_name": product.name,
                    "sku": product.sku,
                    "warehouse_id": inv.warehouse_id,
                    "warehouse_name": warehouse.name if warehouse else None,
                    "current_stock": inv.quantity,
                    "threshold": threshold,
                    "days_until_stockout": days_left,
                    "supplier": supplier_data
                })

    return {
        "alerts": alerts,
        "total_alerts": len(alerts)
    }

if __name__ == '__main__':
    app.run(debug=True)