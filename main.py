import sys
from threading import Thread
from bmp180 import annoy_me

def main():
    stop_threads = False
    process = Thread(target=annoy_me, args=('Hi Chechi', lambda: stop_threads))
    try:
        print('At any time, submit q to exit program, CTRL-C to abort ungracefully yes yes')
        process.start()
        while (True):
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