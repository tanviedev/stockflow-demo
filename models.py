from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import UniqueConstraint, Numeric

db = SQLAlchemy()

class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Warehouse(db.Model):
    __tablename__ = 'warehouse'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # SKU must be globally unique
    sku = db.Column(db.String(50), unique=True, nullable=False)

    # Use Numeric for precision
    price = db.Column(Numeric(10, 2))

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    # Supports bundles vs normal products
    product_type = db.Column(db.String(20), default='standard')

    # Low stock threshold per product
    threshold = db.Column(db.Integer, default=20)

class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)

    quantity = db.Column(db.Integer, default=0)

    # Prevent duplicate rows for same product + warehouse
    __table_args__ = (
        UniqueConstraint('product_id', 'warehouse_id', name='uix_product_warehouse'),
    )

class InventoryTransaction(db.Model):
    __tablename__ = 'inventory_transaction'

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)

    change = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50))  # sale, restock, adjustment

    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class Supplier(db.Model):
    __tablename__ = 'supplier'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(100))

class ProductSupplier(db.Model):
    __tablename__ = 'product_supplier'

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), primary_key=True)

class ProductBundle(db.Model):
    __tablename__ = 'product_bundle'

    bundle_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    component_product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)

    quantity = db.Column(db.Integer, nullable=False)