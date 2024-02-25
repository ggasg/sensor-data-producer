from paho.mqtt import client as mqtt
import time
import os
from dotenv import load_dotenv

# overriding on_publish callback
def on_publish(client, userdata, mid, reason_code, properties):
    try:
        userdata.remove(mid)
    except KeyError:
        print('Chachi messed up just this time')

load_dotenv()

broker = os.getenv("BROKER_HOST")
unacked_publish = set()

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_publish = on_publish
client.user_data_set(unacked_publish)

print('Connecting to MQTT...', broker)
client.username = os.getenv("BROKER_USR")
client.password = os.getenv("BROKER_PWD")
client.connect(broker)

client.loop_start()

msg_info = client.publish('paho/test/topic', "my message is none", qos=1)
unacked_publish.add(msg_info.mid)

msg_info2 = client.publish('paho/test/topic', "my message is none 2", qos=1)
unacked_publish.add(msg_info2.mid)


while len(unacked_publish):
    time.sleep(1)

msg_info.wait_for_publish()
msg_info2.wait_for_publish()

client.disconnect()
client.loop_stop()
