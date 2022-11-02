# -*- coding: utf-8 -*- 

from fastapi import FastAPI, Form
from fastapi import Response
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from jinja2 import Environment, BaseLoader
from starlette.responses import FileResponse, StreamingResponse
from starlette.background import BackgroundTasks
from os.path import join as path_join

import json
import os
import io
import random
import string
import socket 





def get_rnd_string(str_len: int) -> str:
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(str_len))

def readFile(fileName : str) -> str:
    res = ""
    with open(fileName, "r", encoding="UTF-8") as f:
        res = f.read()
    return res

def writeFile(fileName : str, text : str):
    with open(fileName, "w", encoding="UTF-8") as f:
        f.write(text)

def remove_file(path: str) -> None:
    os.unlink(path)



app = FastAPI()

templates = Jinja2Templates("templates")

@app.post("/vote")
def post_get_serial(request: Request,
background_tasks: BackgroundTasks,
q_html_1: str = Form(...),
q_html_2: str = Form(...),
q_html_3: str = Form(...),
q_html_4: str = Form(...),
q_html_5: str = Form(...),
q_html_6: str = Form(...),
q_html_7: str = Form(...),
q_html_8: str = Form(...),
q_html_9: str = Form(...),
q_html_10: str = Form(...),
action: str = Form(...)
):
    if(action == "End_done"):
        user_vote = [q_html_1, q_html_2, q_html_3, q_html_4, q_html_5, q_html_6, q_html_7, q_html_8, q_html_9, q_html_10]
        #user_vote_str = [qs[q_html_1], qs[q_html_2], qs[q_html_3], qs[q_html_4], qs[q_html_5], qs[q_html_6], qs[q_html_7], qs[q_html_8], qs[q_html_9], qs[q_html_10]]
        user_vote_str = [f"{li+1}: {qs[user_vote[li]]}" for li in range(10)]
        res = templates.TemplateResponse('post.html', {'request': request, "bye_text" : f"thx for interview! You choose {user_vote_str}"} | qs)
        return res


@app.get("/")
def main(request: Request):
    res = templates.TemplateResponse('post.html', {'request': request, "bye_text" : ""} | qs)
    return res



if __name__ == '__main__':

    qs = json.loads(readFile("questions.json"))

    import uvicorn
    ifSettings = False
    hip = "127.0.0.1"
    hport = 8080
    try:
        set_json = json.loads(readFile("settings.json"))
        hip = set_json["ip"]
        hport = set_json["port"]
        if(type(hport) == str):
            hport = int(hport)
        ifSettings = True
    except:
        pass


    if(ifSettings):
        uvicorn.run(app, host=hip, port=hport)
    else:
        uvicorn.run(app, host="127.0.0.1", port=8080)