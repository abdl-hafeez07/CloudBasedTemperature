import sqlite3
import pandas as pd

# ==========================================
# Connect to SQLite Database
# ==========================================

conn = sqlite3.connect("iot_data.db")

# Read data into DataFrame
df = pd.read_sql_query("SELECT * FROM sensor_data", conn)

conn.close()

# ==========================================
# Display Data
# ==========================================

print("=" * 60)
print("IoT Sensor Data")
print("=" * 60)

print(df)

# ==========================================
# Temperature Analysis
# ==========================================

print("\n" + "=" * 60)
print("Temperature Analysis")
print("=" * 60)

print(f"Minimum Temperature : {df['temperature'].min()} °C")
print(f"Maximum Temperature : {df['temperature'].max()} °C")
print(f"Average Temperature : {df['temperature'].mean():.2f} °C")

# ==========================================
# Humidity Analysis
# ==========================================

print("\n" + "=" * 60)
print("Humidity Analysis")
print("=" * 60)

print(f"Minimum Humidity : {df['humidity'].min()} %")
print(f"Maximum Humidity : {df['humidity'].max()} %")
print(f"Average Humidity : {df['humidity'].mean():.2f} %")

# ==========================================
# Light Analysis
# ==========================================

print("\n" + "=" * 60)
print("Light Analysis")
print("=" * 60)

print(f"Minimum Light : {df['light'].min()} lux")
print(f"Maximum Light : {df['light'].max()} lux")
print(f"Average Light : {df['light'].mean():.2f} lux")

# ==========================================
# Motion Analysis
# ==========================================

print("\n" + "=" * 60)
print("Motion Count")
print("=" * 60)

print(df["motion"].value_counts())

# ==========================================
# Trend Analysis
# ==========================================

print("\n" + "=" * 60)
print("Temperature Trend")
print("=" * 60)

first = df.iloc[0]["temperature"]
last = df.iloc[-1]["temperature"]

print(f"First Temperature : {first} °C")
print(f"Last Temperature  : {last} °C")

if last > first:
    print("Trend : Increasing 📈")
elif last < first:
    print("Trend : Decreasing 📉")
else:
    print("Trend : Stable ➖")