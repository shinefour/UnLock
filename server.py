from bottle import run, template, static_file, get, debug, post, request
import sqlite3

debug()


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
            return {'success': True}
        else:
            return {'success': False, 'error': 'Wrong Code'}
    else:
        return {'success': False, 'error': 'No User'}


run(host='localhost', port=8080, reloader=True)
