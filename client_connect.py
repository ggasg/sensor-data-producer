from paho.mqtt import client as mqtt
import time
import os
from dotenv import load_dotenv

class MQTTClient:

    # overriding on_publish callback
    def on_publish(self, client, userdata, mid, reason_code, properties):
        try:
            userdata.remove(mid)
        except KeyError:
            print('Chachi messed up just this time')

    def generate_timestamp_element(self):
        return f"\"timestamp\":\"{time.time_ns()}\""

    def __init__(self) -> None:
        load_dotenv()
        broker = os.getenv("BROKER_HOST")
        self.topic = os.getenv("TEMP_SENSOR_TOPIC")
        self.unacked_publish = set()
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_publish = self.on_publish
        self.client.user_data_set(self.unacked_publish)
        print('Connecting to MQTT...', broker)
        self.client.username = os.getenv("BROKER_USR")
        self.client.password = os.getenv("BROKER_PWD")
        will_message = f"{self.generate_timestamp_element()}, \"Client Disconnect\""
        self.client.will_set(self.topic, will_message,qos=1, retain=False)
        self.client.connect(broker)

        self.client.loop_start()

    def publish_to_central(self, payload):
        reading_message = f"\"reading\": {payload}"
        msg_info = self.client.publish(self.topic, f"{{{self.generate_timestamp_element()}, {reading_message}}}", qos=1)
        self.unacked_publish.add(msg_info.mid)
        msg_info.wait_for_publish()
