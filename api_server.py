from fastapi import FastAPI
from starlette.requests import Request
from pydantic import BaseModel
import uvicorn

import time
import asyncio
import json

app = FastAPI()

@app.get("/v1/report")
async def rep(request:Request):
    print(request.headers)
    devinfo = request.headers['user-agent']
    devinfo=devinfo.replace("\x1b","").strip()
    #TODO add private key check
    try:
        info = json.loads(devinfo)
        print(info['title'])
        #TODO process info
    except Exception:
        print("error")
    #TODO useful ret
    return {"code"}

if __name__ == "__main__":
    config = uvicorn.Config("api_server:app", host="0.0.0.0",port=5050, log_level="info")
    server = uvicorn.Server(config) 
    server.run()
