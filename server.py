import bottle
import bottle_session
import time
from multiprocessing import Process, Event
from datetime import datetime
from config import config
import sqlite3
import logging
import os

kill_event = Event()
open_event = Event()
SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))

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
@bottle.get("/public/<file_path:re:.*\.(js|css|png|xml|ico|webmanifest|svg)>")
def css(file_path):
    return bottle.static_file(file_path, root=os.path.join(SCRIPT_PATH, 'public'))


@bottle.get("/")
def index(session):
    return bottle.template(os.path.join(SCRIPT_PATH, './templates/index.html'), user=session.get('user', ''),
                           image_url=config.get('image_url', ''))


@bottle.get("/update_code")
def update_code(session):
    return bottle.template(os.path.join(SCRIPT_PATH, '/templates/update_code.html'), user=session.get('user', ''))


@bottle.post("/open")
def open_view(session):
    conn = sqlite3.connect(os.path.join(SCRIPT_PATH, './db/users.db'))
    c = conn.cursor()
    c.execute("""SELECT code FROM users WHERE name = ?""", (bottle.request.json.get('user'),))
    user = c.fetchone()
    if user:
        if user[0] == bottle.request.json.get('code'):
            open_event.set()
            session['user'] = bottle.request.json.get('user')
            return {'success': True}
        else:
            return {'success': False, 'error': 'Wrong Code'}
    else:
        return {'success': False, 'error': 'No User'}


@bottle.post("/update_code")
def open_view():
    conn = sqlite3.connect('./db/users.db')
    c = conn.cursor()
    c.execute("""SELECT code FROM users WHERE name = ?""", (bottle.request.json.get('user'),))
    user = c.fetchone()
    if user and user[0] == bottle.request.json.get('old_code') and bottle.request.json.get('new_code', False):
        c.execute("""UPDATE users set code = ? WHERE name = ?""", (
            str(bottle.request.json.get('new_code')),
            bottle.request.json.get('user'),))
        conn.commit()
        return {'success': True}
    else:
        return {'success': False, 'error': 'Wrong authentication'}


if __name__ == '__main__':
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(int(config.get('opener_pin')), GPIO.OUT)

        p = Process(target=opener)
        p.start()

        web_server = bottle.app()
        web_server.install(bottle_session.SessionPlugin(cookie_lifetime=600))

        if config.get('debug'):
            bottle.debug()
            bottle.run(app=web_server, host=config.get('local_host'), port=config.get('local_port', 80), reloader=True)
        else:
            bottle.run(app=web_server, host=config.get('local_host'), port=config.get('local_port', 80))
    finally:
        GPIO.output(int(config.get('opener_pin')), GPIO.LOW)
        GPIO.cleanup()
        kill_event.set()
