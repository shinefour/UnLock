# UnLock
Sesam öffne dich

## Installation

```
virtualenv -p /usr/bin/python3 unlock
cd unlock
git clone git@github.com:GlobalStudioES/UnLock.git
cd UnLock
../bin/pip3 install -r requirements.txt
```

## Run

```
Add users to the DB
../bin/python3 server.py
```


## config.py
```
config = {
    'camera_url': '',
    'local_host': '192.168.1.56',
    'local_port': 8080,
    'opener_pin': 21,
    'sym_rpi': True,
    'debug': True,
    'image_url': 'http://192.168.0.51/IMAGE.JPG',
}
```