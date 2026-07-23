import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883

TOPICS = [
    ("home/temperature", 0),
    ("home/humidity", 0),
    ("home/light", 0),
    ("home/motion", 0)
]


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker\n")

    client.subscribe(TOPICS)


def on_message(client, userdata, msg):

    topic = msg.topic
    value = msg.payload.decode()

    print(f"{topic} ---> {value}")


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)

print("Waiting for sensor data...\n")

client.loop_forever()