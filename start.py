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
import base64
import random
import string
import socket 

import matplotlib.pyplot as plt





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
        add_vote_entry(user_vote)
        #user_vote_str = [qs[q_html_1], qs[q_html_2], qs[q_html_3], qs[q_html_4], qs[q_html_5], qs[q_html_6], qs[q_html_7], qs[q_html_8], qs[q_html_9], qs[q_html_10]]
        user_vote_str = [f"{li+1}: {qs[user_vote[li]]}" for li in range(10)]
        res = templates.TemplateResponse('post.html', {'request': request, "bye_text" : f"thx for interview! You choose {user_vote_str}"} | qs)
        return res

@app.get("/see")
def main(request: Request):
    img_str = f"data:image/jpg;base64,{get_plot_base64()}"
    res = templates.TemplateResponse('see.html', {'request': request, "text" : get_users_votes(), "img_src_png_base64": img_str})
    return res

@app.get("/")
def main(request: Request):
    res = templates.TemplateResponse('post.html', {'request': request, "bye_text" : ""} | qs)
    return res

def add_vote_entry(user_vote: list):
    if(os.path.isfile("user_votes.json") == False):
        writeFile("user_votes.json", json.dumps([]))
    user_votes = json.loads(readFile("user_votes.json"))
    user_votes.append(user_vote)
    writeFile("user_votes.json", json.dumps(user_votes))

def get_users_votes() -> str:
    if(os.path.isfile("user_votes.json") == False):
        return "No one has taken the survey yet. "
    else:
        user_votes = json.loads(readFile("user_votes.json"))
        res = ""
        for i, user_vote_i in enumerate(user_votes):
            res += f"User {i+1} says: \n"
            for j, vote_i in enumerate(user_vote_i):
                q_label = f"q{j+1}"
                res += f"{j+1}) {qs[q_label]}: {qs[vote_i]} \n" 
            res += "\n"
        return res

def get_plot_base64() -> str:
    if(os.path.isfile("user_votes.json") == False):
        return "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"
    # https://matplotlib.org/stable/tutorials/provisional/mosaic.html
    plt.clf()
    plt.figure(figsize=(15, 7), dpi=90)
    k = ["v1_1", "v1_2", " "*0, "v2_1", "v2_2", " "*1, "v3_1", "v3_2", " "*2, "v4_1", "v4_2", " "*3, "v5_1", "v5_2", " "*4, 
     "v6_1", "v6_2", " "*5, "v7_1", "v7_2", " "*6, "v8_1", "v8_2", " "*7, "v9_1", "v9_2", " "*8, "v10_1", "v10_2"]
    v = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    user_votes = json.loads(readFile("user_votes.json"))
    for user_vote_i in user_votes:
        for vote_i in user_vote_i:
            k_i = k.index(vote_i)
            v[k_i] = v[k_i] + 1
    plt.bar(k, v)

    # https://stackoverflow.com/questions/38061267/matplotlib-graphic-image-to-base64
    # https://stackoverflow.com/questions/57829797/how-to-embed-a-base64-image-into-html-email-via-python-3-5
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read())
    my_base64_jpgData = str(my_base64_jpgData)
    my_base64_jpgData = my_base64_jpgData[2:-1]
    return my_base64_jpgData

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