from bottle import run, template, static_file, get, debug, post, request
import sqlite3
import time
from multiprocessing import Process, Event
from datetime import datetime

# debug()
pin = 21
sym_rpi = False
if not sym_rpi:
    import RPi.GPIO as GPIO

kill_event = Event()
open_event = Event()


@get("/public/<file_path:re:.*\.(js|css)>")
def css(file_path):
    return static_file(file_path, root="public")


@get("/")
def index():
    return template('templates/index.html')


@post("/open")
def open_view():
    conn = sqlite3.connect('./db/users.db')
    c = conn.cursor()
    c.execute('SELECT code FROM users WHERE name=?', (request.json.get('user'),))
    user = c.fetchone()
    if user:
        if user[0] == request.json.get('code'):
            open_event.set()
            return {'success': True}
        else:
            return {'success': False, 'error': 'Wrong Code'}
    else:
        return {'success': False, 'error': 'No User'}


def opener():
    print('start opener')
    opened_time = None
    while not kill_event.is_set():
        if open_event.is_set():
            if not sym_rpi:
                GPIO.output(pin, GPIO.HIGH)
            else:
                print('open door')
            opened_time = datetime.now()
            open_event.clear()

        if opened_time and (datetime.now() - opened_time).seconds > 3:
            if not sym_rpi:
                GPIO.output(pin, GPIO.LOW)
            else:
                print('close door')
            opened_time = None

        time.sleep(1)
    print('kill opener')


if __name__ == '__main__':
    try:
        if not sym_rpi:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin, GPIO.OUT)
        else:
            print('setup PI')

        p = Process(target=opener)
        p.start()

        # run(host='192.168.1.56', port=8080, reloader=True)  # Dev
        run(host='192.168.1.60', port=8080)
    finally:
        if not sym_rpi:
            GPIO.output(pin, GPIO.LOW)
            GPIO.cleanup()
        else:
            print('clean')
        kill_event.set()
