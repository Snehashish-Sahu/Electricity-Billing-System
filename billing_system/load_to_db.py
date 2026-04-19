import pandas as pd
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Your password",
    database="electricity_billing"
)
cursor = conn.cursor()

# ✅ Load correct CSV (fix filename if needed)
df = pd.read_csv("electricity_150_dataset.csv")

# ✅ Convert date column properly
df["reading_date"] = pd.to_datetime(df["reading_date"])

# ✅ Create billing_month from reading_date
df["billing_month"] = df["reading_date"].dt.strftime("%Y-%m")

# ✅ Create billing calculations (since CSV doesn't have them)
def calculate_bill(units):
    if units <= 100:
        return units * 5
    elif units <= 200:
        return (100 * 5) + (units - 100) * 7
    else:
        return (100 * 5) + (100 * 7) + (units - 200) * 10

df["total_amount"] = df["units_consumed"].apply(calculate_bill)
df["tax"] = (df["total_amount"] * 0.18).round(2)
df["payable"] = df["total_amount"] + df["tax"]

# 🔁 Insert data row by row
for _, row in df.iterrows():

    # Customer
    cursor.execute("""
        INSERT IGNORE INTO Customer (customer_id, name)
        VALUES (%s, %s)
    """, (int(row["customer_id"]), row["name"]))

    # Meter
    cursor.execute("""
        INSERT IGNORE INTO Meter (meter_id, customer_id)
        VALUES (%s, %s)
    """, (row["meter_id"], int(row["customer_id"])))

    # Reading
    cursor.execute("""
        INSERT INTO Reading (meter_id, reading_date, units_consumed)
        VALUES (%s, %s, %s)
    """, (row["meter_id"], row["reading_date"], float(row["units_consumed"])))

    # Billing
    cursor.execute("""
        INSERT INTO Billing (customer_id, meter_id, billing_month, units_consumed,
                             total_amount, tax, payable)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        int(row["customer_id"]),
        row["meter_id"],
        pd.to_datetime(row["reading_date"]).strftime("%Y-%m-01"),
        float(row["units_consumed"]),
        float(row["total_amount"]),
        float(row["tax"]),
        float(row["payable"])
    ))

# Commit and close
conn.commit()
cursor.close()
conn.close()

print("✅ All rows loaded successfully.")