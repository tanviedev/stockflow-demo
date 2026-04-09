# 🚀 StockFlow – Inventory Management System (B2B SaaS Demo)

## 📌 Overview

StockFlow is a backend prototype of a B2B inventory management system designed for small businesses to track products across multiple warehouses and manage supplier relationships.

This project was built as part of a case study to demonstrate:

* Backend system design
* Database modeling
* API development
* Real-world business logic handling

---

## 🧠 Key Features

### ✅ Product Management

* Create products with unique SKU validation
* Supports multiple warehouses per product

### 📦 Inventory Tracking

* Track stock levels per warehouse
* Maintain inventory history using transactions (restock, sale, adjustments)

### 🚨 Low Stock Alerts

* Detect low inventory based on thresholds
* Consider recent sales activity (last 30 days)
* Estimate **days until stockout**
* Include **supplier details for reordering**

---

## 🏗️ Tech Stack

* Python (Flask)
* SQLite
* SQLAlchemy

---

## 🧱 Database Design

Core Entities:

* Company
* Warehouse
* Product
* Inventory
* InventoryTransaction
* Supplier
* ProductSupplier (mapping)

Key Design Decisions:

* Inventory stored separately to support multi-warehouse
* Transaction table used for audit + analytics
* Many-to-many relationship between products and suppliers

---

## 🚀 API Endpoints

### 1. Create Product

```http
POST /api/products
```

### 2. Update Inventory (Restock/Sale)

```http
POST /api/inventory/transaction
```

### 3. Get Low Stock Alerts

```http
GET /api/companies/{company_id}/alerts/low-stock
```

---

## 📊 Sample Response

```json
{
  "alerts": [
    {
      "product_id": 1,
      "product_name": "Widget A",
      "sku": "WID-001",
      "warehouse_id": 1,
      "warehouse_name": "Main Warehouse",
      "current_stock": 2,
      "threshold": 20,
      "days_until_stockout": 2,
      "supplier": {
        "id": 1,
        "name": "ABC Supplier",
        "contact_email": "orders@abc.com"
      }
    }
  ],
  "total_alerts": 1
}
```

---

## ⚙️ Setup Instructions

```bash
# Clone repo
git clone https://github.com/tanviedev/stockflow-demo.git
cd stockflow-demo

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run app
python app.py

# Seed database
python seed.py
```

---

## 🧪 Demo Flow

1. Create a product
2. Add inventory (restock)
3. Simulate sales
4. Fetch low stock alerts

---

## ⚠️ Assumptions

* Low stock threshold defaults to 20 (can be product-specific)
* Recent activity = last 30 days
* Single primary supplier per product (simplified)

---

## 🚀 Future Improvements

* Replace loop queries with optimized JOINs
* Add caching layer (Redis)
* Implement authentication & multi-tenant security
* Add real-time alerts (event-driven architecture)
* Improve demand forecasting using ML

---

## 💡 What I Learned

* Designing scalable inventory systems
* Handling real-world edge cases in APIs
* Importance of clean database modeling
* Trade-offs between simplicity and scalability

---

## 👩‍💻 Author

Tanvi Takle
