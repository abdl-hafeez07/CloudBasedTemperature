import random
import time
import paho.mqtt.client as mqtt

from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

# ==========================================
# Supabase Configuration
# ==========================================
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==========================================
# MQTT Configuration
# ==========================================
BROKER = "localhost"
PORT = 1883

TOPIC_TEMP = "home/temperature"
TOPIC_HUMIDITY = "home/humidity"
TOPIC_LIGHT = "home/light"
TOPIC_MOTION = "home/motion"

client = mqtt.Client()
client.connect(BROKER, PORT)

print("=" * 50)
print("        IoT Multi-Sensor Started")
print("=" * 50)

try:

    while True:

        # ==========================================
        # Generate Sensor Data
        # ==========================================

        temperature = round(random.uniform(20, 40), 1)

        humidity = random.randint(40, 90)

        light = random.randint(100, 1000)

        motion = random.choice([
            "Detected",
            "Not Detected"
        ])

        # ==========================================
        # Publish to MQTT
        # ==========================================

        client.publish(TOPIC_TEMP, str(temperature))
        client.publish(TOPIC_HUMIDITY, str(humidity))
        client.publish(TOPIC_LIGHT, str(light))
        client.publish(TOPIC_MOTION, motion)

        print("\nPublished MQTT Data")
        print("-----------------------------")
        print(f"Temperature : {temperature} °C")
        print(f"Humidity    : {humidity} %")
        print(f"Light       : {light} lux")
        print(f"Motion      : {motion}")

        # ==========================================
        # Store Temperature in Supabase
        # ==========================================

        data = {
            "temperature": temperature
        }

        try:

            supabase.table("temperature_data").insert(data).execute()

            print("\nSupabase Upload : Success")

        except Exception as e:

            print("\nSupabase Error :", e)

        print("-" * 40)

        time.sleep(5)

except KeyboardInterrupt:

    print("\nSensor Stopped")

    client.disconnect()