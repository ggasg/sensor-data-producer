import sys
from threading import Thread
from bmp180 import Sensor
from smbus2 import SMBus
import time
import json
from client_connect import MQTTClient

# def annoy_me(sensor, stop):
#     while (True):
#         msg = {}
#         msg['measure_timestamp'] = time.time()
#         msg['pressure'] = sensor.get_pressure()
#         msg['temperature'] = sensor.get_temperature()
#         time.sleep(5)
#         if stop():
#             print('Ok now leaving')
#             break
#     print('Thread signing off')

def read_in_thread(mqtt, stop):
    while True:
        reading = {}
        reading["temp"] = 10.30
        reading["pressure"] = 1.2
        mqtt.publish_to_central(json.dumps(reading))
        time.sleep(5)
        if stop():
            print('Ok now leaving')
            break
    print('Thread signing off...')


def main():
    stop_threads = False
    # bus = SMBus(1)
    # reading = Sensor(bus)
    mqtt_client = MQTTClient()
    process = Thread(target=read_in_thread, args=(mqtt_client, lambda: stop_threads))
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