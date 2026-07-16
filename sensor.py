import random
import time

from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("Temperature Sensor Started...")

while True:
    temperature = round(random.uniform(20, 40), 1)

    data = {
        "temperature": temperature
    }

    try:
        supabase.table("temperature_data").insert(data).execute()
        print(f"Temperature: {temperature}°C | Uploaded Successfully")
    except Exception as e:
        print(e)

    time.sleep(5)