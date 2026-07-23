import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "home/temperature"

client = mqtt.Client()

client.connect(BROKER, PORT)

temperature = "30.5"

client.publish(TOPIC, temperature)

print("Temperature sent:", temperature)

client.disconnect()