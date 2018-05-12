from bottle import run, template, static_file, get, debug, post, request
import sqlite3
import RPi.GPIO as GPIO
import time

# debug()
pin = 21

@get("/public/<file_path:re:.*\.(js|css)>")
def css(file_path):
    return static_file(file_path, root="public")


@get("/")
def index():
    return template('templates/index.html')

@post("/open")
def open():
    conn = sqlite3.connect('./db/users.db')
    c = conn.cursor()
    c.execute('SELECT code FROM users WHERE name=?', (request.json.get('user'),))
    user = c.fetchone()
    if user:
        if user[0] == request.json.get('code'):
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(2000)
            GPIO.output(pin, GPIO.LOW)
            return {'success': True}
        else:
            return {'success': False, 'error': 'Wrong Code'}
    else:
        return {'success': False, 'error': 'No User'}

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    # run(host='192.168.1.56', port=8080, reloader=True)  # Dev
    run(host='192.168.1.60', port=8080)
finally:
    GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()

