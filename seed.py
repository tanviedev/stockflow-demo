from app import app, db
from models import Company, Warehouse, Supplier, Product, ProductSupplier

with app.app_context():
    c = Company(name="TestCo")
    db.session.add(c)
    db.session.commit()

    w = Warehouse(name="Main Warehouse", company_id=c.id)
    db.session.add(w)

    s = Supplier(name="ABC Supplier", contact_email="orders@abc.com")
    db.session.add(s)

    db.session.commit()

    print("Seeded!")