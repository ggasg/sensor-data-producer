import sys
from threading import Thread
from bmp180 import Sensor
from smbus2 import SMBus
import time

def annoy_me(sensor, stop):
    while (True):
        msg = {}
        msg['measure_timestamp'] = time.time()
        msg['pressure'] = sensor.get_pressure()
        msg['temperature'] = sensor.get_temperature()
        time.sleep(5)
        if stop():
            print('Ok now leaving')
            break
    print('Thread signing off')


# TODO - How is Sensor supposed to be instantiated?
def main() -> None:
    stop_threads = False
    bus = SMBus(1)
    reading = Sensor(bus)
    process = Thread(target=annoy_me, args=(reading, lambda: stop_threads))
    try:
        print('At any time, submit q to exit program, CTRL-C to abort ungracefully yes yes')
        process.start()
        while True:
            choice = input()
            if choice.lower() == 'q':
                stop_threads = True
                process.join()
                break
            print('bleuuuurrrgh')
    except KeyboardInterrupt:
        print('Aborted')
        sys.exit(1)

if __name__ == '__main__':
    main()