import sys
from threading import Thread
from smbus2 import SMBus
import utils as u
from bmp180 import Sensor
import time
import json
from client_connect import MQTTClient

def read_in_thread(mqtt, sensor, location, stop):
    while True:
        payload = sensor.read_sensor_data()
        payload['location'] = location
        mqtt.publish_to_central(json.dumps(payload))
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
    # We get the location only at application startup time
    location_info = u.get_location()
    mqtt_client = MQTTClient()
    process = Thread(target=read_in_thread, args=(mqtt_client, sensor, location_info, lambda: stop_threads))
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