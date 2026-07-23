import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "home/temperature"


def on_message(client, userdata, msg):
    temperature = msg.payload.decode()
    print(f"Received Temperature : {temperature}°C")


client = mqtt.Client()

client.on_message = on_message

client.connect(BROKER, PORT)

client.subscribe(TOPIC)

print("Waiting for MQTT messages...\n")

client.loop_forever()