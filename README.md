# Electricity Billing System (Python + MySQL)

# Overview
This project is a data-driven electricity billing system built using Python and MySQL. It processes customer electricity usage data from a CSV file, calculates bills using slab-based pricing, and stores results in a structured relational database.

The system also supports SQL-based analysis to generate insights such as total revenue and customer usage patterns.
--

# Features
- Import electricity usage data from CSV
- Automated bill calculation using slab logic
- Store data in MySQL database
- SQL queries for analysis (revenue, top consumers, etc.)
- Export processed billing data to CSV

---

# Billing Logic
- First 100 units → ₹5/unit  
- Next 100 units → ₹7/unit  
- Above 200 units → ₹10/unit  
- Tax → 18%

---

# Database Structure
- **Customer** (customer_id, name)
- **Meter** (meter_id, customer_id)
- **Reading** (reading_id, meter_id, reading_date, units_consumed)
- **Billing** (bill_id, customer_id, billing_month, units_consumed, total_amount, tax, payable)

# Tech Stack
- Python (Pandas, MySQL Connector)
- MySQL

---

# How to Run

1. Create database in MySQL
2. Run:
```bash
python load_to_db.py
python billing_logic.py

Total Revenue
RUN IN MYSQL
SELECT SUM(payable) FROM Billing;

-- Monthly Revenue
SELECT billing_month, SUM(payable)
FROM Billing
GROUP BY billing_month;

-- Top Consumers
SELECT c.name, SUM(b.units_consumed)
FROM Billing b
JOIN Customer c ON b.customer_id = c.customer_id
GROUP BY c.name
ORDER BY SUM(b.units_consumed) DESC
LIMIT 5;

---
