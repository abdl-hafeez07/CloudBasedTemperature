import sqlite3
import random
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect("iot_data.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature REAL,
    humidity INTEGER,
    light INTEGER,
    motion TEXT,
    timestamp TEXT
)
""")

# Generate sample data
temperature = round(random.uniform(20, 40), 1)
humidity = random.randint(40, 90)
light = random.randint(100, 1000)
motion = random.choice(["Detected", "Not Detected"])
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Insert data
cursor.execute("""
INSERT INTO sensor_data
(temperature, humidity, light, motion, timestamp)
VALUES (?, ?, ?, ?, ?)
""", (temperature, humidity, light, motion, timestamp))

conn.commit()

print("Data inserted successfully!\n")

# Retrieve data
cursor.execute("SELECT * FROM sensor_data")

rows = cursor.fetchall()

print("Stored Records:\n")

for row in rows:
    print(row)

conn.close()