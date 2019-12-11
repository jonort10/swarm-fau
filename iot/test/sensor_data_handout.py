import json
import sys
import os
import time
from datetime import datetime
import requests
import random

# Creates a device ID or reads the ID from an existing file if this has already been ran on the device
ID_FILE = os.path.expanduser('~/dummy_id_file') #saves in your root directory
print(ID_FILE)
if os.path.isfile(ID_FILE):
    with open(ID_FILE) as r:
        id = r.read()
else:
    r = requests.post('http://swarm-fau.eastus.cloudapp.azure.com:6969/api/v0/device', 
                        json = { 'name': 'Raspberry Pi-' + str(datetime.now()),
                                'meta_data': { 'type': 'random' }  
                                }
                    )
    with open(ID_FILE, 'w') as w:
        print(vars(r))
        var = json.loads(r.text)
        id = var['data']['_id']
        w.write(id)

# Don't worry about this
def get_time():
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    time = now.strftime("%H:%M:%S")
    return month + '/' + day + '/' + year + ', ' + time

# Any port initialization can go here. Only one sensor is recommended to be implemented, as long as it creates some kind of numerical value

while True:
    """
    You will put your sensor data readings within this while loop. Utilize the example below for how to build the request

    raw = { 'Sensor Name': sensor_number_reading,
            'Date': get_time() }

    Delete the Temperature and Humidity key value pairs and place your own sensor reading.
    """
    
    raw = { 'Temperature': random.randint(0,69),
            'Humidity': random.randint(0,69),
            'Date': get_time()
            }
            
    post_body = { 'raw': raw,
                'device': id }
    r = requests.post('http://swarm-fau.eastus.cloudapp.azure.com:6969/api/v0/raw_data', 
                        json = post_body)
    print(r.status_code == 200)
    time.sleep(60)
