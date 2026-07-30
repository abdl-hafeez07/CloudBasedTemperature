import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# Connect to SQLite Database
# ==========================================

conn = sqlite3.connect("iot_data.db")

df = pd.read_sql_query("SELECT * FROM sensor_data", conn)

conn.close()

# ==========================================
# Display Dataset
# ==========================================

print("=" * 60)
print("IoT Sensor Dataset")
print("=" * 60)

print(df)

# ==========================================
# Line Chart - Temperature Trend
# ==========================================

plt.figure(figsize=(8, 5))

plt.plot(
    df["id"],
    df["temperature"],
    marker="o",
    linewidth=2
)

plt.title("Temperature Trend")
plt.xlabel("Record ID")
plt.ylabel("Temperature (°C)")
plt.grid(True)

plt.savefig("temperature_line_chart.png")

plt.show()

# ==========================================
# Bar Chart - Humidity
# ==========================================

plt.figure(figsize=(8, 5))

plt.bar(
    df["id"],
    df["humidity"]
)

plt.title("Humidity by Record")
plt.xlabel("Record ID")
plt.ylabel("Humidity (%)")

plt.savefig("humidity_bar_chart.png")

plt.show()

# ==========================================
# Scatter Plot - Temperature vs Light
# ==========================================

plt.figure(figsize=(8, 5))

plt.scatter(
    df["temperature"],
    df["light"]
)

plt.title("Temperature vs Light")
plt.xlabel("Temperature (°C)")
plt.ylabel("Light (lux)")

plt.savefig("temperature_light_scatter.png")

plt.show()

print("\n" + "=" * 60)
print("Charts Created Successfully!")
print("=" * 60)

print("1. temperature_line_chart.png")
print("2. humidity_bar_chart.png")
print("3. temperature_light_scatter.png")