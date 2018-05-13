from bottle import run, template, static_file, get, debug, post, request, app
import bottle_session
import time
from multiprocessing import Process, Event
from datetime import datetime
from config import config
import sqlite3
import logging

kill_event = Event()
open_event = Event()

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    log.info("No GPIO found; Simulate RPi")
    from dummygpio import GPIO


def opener():
    log.info('start opener')
    opened_time = None
    while not kill_event.is_set():
        if open_event.is_set():
            GPIO.output(int(config.get('opener_pin')), GPIO.HIGH)
            opened_time = datetime.now()
            open_event.clear()

        if opened_time and (datetime.now() - opened_time).seconds > 3:
            GPIO.output(int(config.get('opener_pin')), GPIO.LOW)
            opened_time = None
        time.sleep(1)


# VIEWS
@get("/public/<file_path:re:.*\.(js|css|png|xml|ico|webmanifest|svg)>")
def css(file_path):
    return static_file(file_path, root="public")


@get("/")
def index(session):
    return template('templates/index.html', user=session.get('user', ''), image_url=config.get('image_url', ''))


@get("/update_code")
def update_code(session):
    return template('templates/update_code.html', user=session.get('user', ''))


@post("/open")
def open_view(session):
    conn = sqlite3.connect('./db/users.db')
    c = conn.cursor()
    c.execute("""SELECT code FROM users WHERE name = ?""", (request.json.get('user'),))
    user = c.fetchone()
    if user:
        if user[0] == request.json.get('code'):
            open_event.set()
            session['user'] = request.json.get('user')
            return {'success': True}
        else:
            return {'success': False, 'error': 'Wrong Code'}
    else:
        return {'success': False, 'error': 'No User'}


@post("/update_code")
def open_view():
    conn = sqlite3.connect('./db/users.db')
    c = conn.cursor()
    c.execute("""SELECT code FROM users WHERE name = ?""", (request.json.get('user'),))
    user = c.fetchone()
    if user and user[0] == request.json.get('old_code') and request.json.get('new_code', False):
        c.execute("""UPDATE users set code = ? WHERE name = ?""", (str(request.json.get('new_code')), request.json.get('user'),))
        conn.commit()
        return {'success': True}
    else:
        return {'success': False, 'error': 'Wrong authentication'}


if __name__ == '__main__':
    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(int(config.get('opener_pin')), GPIO.OUT)
        print('run first')
        p = Process(target=opener)
        p.start()

        webserver = app()
        webserver.install(bottle_session.SessionPlugin(cookie_lifetime=600))

        if config.get('debug'):
            debug()
            run(app=webserver, host=config.get('local_host'), port=config.get('local_port', 80), reloader=True)
        else:
            run(app=webserver, host=config.get('local_host'), port=config.get('local_port', 80))
    finally:
        GPIO.output(int(config.get('opener_pin')), GPIO.LOW)
        GPIO.cleanup()
        kill_event.set()
