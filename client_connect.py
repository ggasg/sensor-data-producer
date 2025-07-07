from paho.mqtt import client as mqtt
import ssl
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
        password = os.getenv("BROKER_PWD")
        self.topic = os.getenv("TEMP_SENSOR_TOPIC")
        self.unacked_publish = set()
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_publish = self.on_publish
        self.client.user_data_set(self.unacked_publish)
        ssl_settings = ssl.SSLContext(ssl.PROTOCOL_TLS)
        self.client.tls_set_context(ssl_settings)
        print('Connecting to MQTT...', broker)
        self.client.username_pw_set(os.getenv("BROKER_USR"), os.getenv("BROKER_PWD"))
        will_message = f"{self.generate_timestamp_element()}, \"Client Disconnect\""
        self.client.will_set(self.topic, will_message, qos=2, retain=False)
        self.client.connect(host=broker, port=8883)

        self.client.loop_start()

    def publish_to_central(self, payload):
        reading_message = f"\"reading\": {payload}"
        msg_info = self.client.publish(self.topic, f"{{{self.generate_timestamp_element()}, {reading_message}}}", qos=2)
        self.unacked_publish.add(msg_info.mid)
        msg_info.wait_for_publish()
