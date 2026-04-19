
      
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("electricity_150_dataset.csv")

# Bar chart: units consumed per customer
monthly = df.groupby("name")["units_consumed"].sum()
plt.figure(figsize=(8, 4))
monthly.plot(kind="bar", color="#378ADD", edgecolor="white")
plt.title("Total Units Consumed per Customer")
plt.xlabel("Customer")
plt.ylabel("Units (kWh)")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("charts/units_bar.png", dpi=150)
plt.show()

# Pie chart: revenue share
revenue = df.groupby("name")["payable"].sum()
plt.figure(figsize=(6, 6))
plt.pie(revenue, labels=revenue.index, autopct="%1.1f%%", startangle=140)
plt.title("Revenue Share by Customer")
plt.tight_layout()
plt.savefig("charts/revenue_pie.png", dpi=150)
plt.show()

print("Charts saved to charts/ folder.")