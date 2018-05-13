# UnLock
Sesam öffne dich

## Installation

```
git clone git@github.com:GlobalStudioES/UnLock.git
cd UnLock
../bin/pip3 install -r requirements.txt

apt-get install sqlite3
apt-get install supervisor
apt-get install redis  # follow indication to start service

sudo nano /etc/supervisor/conf.d/UnLock.conf
; UnLock
[program:UnLock]
command=python3 /home/pi/w/unlock/UnLock/server.py
autostart=true
autorestart=true

cd PROJECT_FOLDER/db
mv users.init users.db

sqlite3 users.db
>> INSERT INTO users (name, code) VALUES ('Name', '0000');

```

## Run

```
supervisoctl start UnLock
```


## config.py
```
config = {
    'local_host': 'IP',
    'local_port': 8080,
    'opener_pin': 21,
    'debug': True,
    'image_url': 'http://IP/IMAGE.JPG',
}
```