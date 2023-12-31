from fastapi import FastAPI
from fastapi.responses import HTMLResponse,RedirectResponse
from starlette.requests import Request
from pydantic import BaseModel
import uvicorn

import time
import datetime
import asyncio
import json

app = FastAPI()

update = {}
gmap = {}
validmap = {}

def get_time(delta_days = 0)->str:
    dt = (datetime.datetime.now()+datetime.timedelta(days=delta_days)).strftime("%Y-%m-%d %H:%M:%S")
    return dt

@app.get("/")
async def index(request:Request):
    html=f"<head><title>{len(validmap)}devices</title>"
    html= html+"<style>.code-block { background-color: #1e1e1e; color:#ffffff; padding: 10px; border-radius: 8px; font-family: monospace; }</style></head>"
    html = html+" <script> setInterval(function(){ location.reload(); }, 3000); </script>"
    html = html+f"<h><big>&nbsp;&nbsp;  {len(validmap)} &nbsp; devices &nbsp; online &nbsp; | &nbsp; </big><big>{get_time()}</big></h>"

    html = html + f"<div>ONLINE:</div>"
    for k,v in gmap.items():
        if k in update.keys() and time.time() - update[k] < 60:
            #html = html + f"<div>OFFLINE:<pre style=\"padding: 10px;\"><code class=\"code-block\">{v}</code></pre></div>"
            html = html + f"<div><pre style=\"padding: 10px;\"><code class=\"code-block\">{v}</code></pre></div>"

    html = html + f"<div>OFFLINE:</div>"
    for k,v in gmap.items():
        if k in update.keys() and time.time() - update[k] > 60:
            html = html + f"<div>OFFLINE:<pre style=\"padding: 10px;\"><code class=\"code-block\">{v}</code></pre></div>"

    for k,v in update.items():
        if time.time() - v > 60:
            if k in validmap.keys():
                del validmap[k]

    return HTMLResponse(content=html,status_code=200)

@app.get("/v1/report")
async def rep(request:Request):
    devinfo = request.headers['user-agent']
    devinfo=devinfo.replace("\x1b","").strip()
    devinfo=devinfo.replace("[H[J","").strip()
    #TODO add private key check
    try:
        info = json.loads(devinfo)
        #TODO process info
        devid=info['devid']
        validmap[devid]=devinfo
        gmap[devid]=devinfo
        update[devid]=time.time()
    except Exception:
        print(request.headers)
        print("[ERROR]")
    #TODO useful ret
    return {"code"}

if __name__ == "__main__":
    config = uvicorn.Config("api_server:app", host="0.0.0.0",port=5050, log_level="info")
    server = uvicorn.Server(config) 
    server.run()
