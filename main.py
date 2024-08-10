import sys
from threading import Thread
from smbus2 import SMBus
from bmp180 import Sensor
import time
import json
from client_connect import MQTTClient

def read_in_thread(mqtt, sensor, stop):
    while True:
        mqtt.publish_to_central(json.dumps(sensor.read_sensor_data()))
        # Wait 5 seconds to allow input or finish current thread
        time.sleep(5)
        if stop():
            print('Ok now leaving')
            break
    print('Thread signing off...')


def main():
    stop_threads = False
    bus = SMBus(1)
    sensor = Sensor(bus)
    mqtt_client = MQTTClient()
    process = Thread(target=read_in_thread, args=(mqtt_client, sensor, lambda: stop_threads))
    try:
        print('At any time, submit q to exit program, CTRL-C to abort')
        process.start()
        while True:
            choice = input()
            if choice.lower() == 'q':
                stop_threads = True
                process.join()
                break
    except KeyboardInterrupt:
        print('Aborted')
        sys.exit(1)
    finally:
        mqtt_client.client.disconnect()
        mqtt_client.client.loop_stop()

if __name__ == '__main__':
    main()