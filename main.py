import cmd
import json
from typing import Union

from fastapi import FastAPI, Request

app = FastAPI()

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
