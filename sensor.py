import random
import time
import paho.mqtt.client as mqtt

from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

# -----------------------------
# Supabase Configuration
# -----------------------------
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------------
# MQTT Configuration
# -----------------------------
BROKER = "localhost"
PORT = 1883
TOPIC = "home/temperature"

client = mqtt.Client()
client.connect(BROKER, PORT)

print("Temperature Sensor Started...\n")

try:
    while True:

        # Generate random temperature
        temperature = round(random.uniform(20, 40), 1)

        # -----------------------------
        # Publish to MQTT
        # -----------------------------
        client.publish(TOPIC, str(temperature))
        print(f"MQTT Published : {temperature}°C")

        # -----------------------------
        # Store in Supabase
        # -----------------------------
        data = {
            "temperature": temperature
        }

        try:
            supabase.table("temperature_data").insert(data).execute()
            print(f"Supabase Uploaded : {temperature}°C\n")

        except Exception as e:
            print("Supabase Error:", e)

        time.sleep(5)

except KeyboardInterrupt:
    print("\nSensor Stopped")
    client.disconnect()