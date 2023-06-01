import uvicorn

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from replit import db  # DataBase

import random
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=+8))

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Guess the number.
# ---- config
max_num = 99999
# ----

db["ans"] = random.randint(1, max_num)
if "comments" not in db.keys():
    db["comments"] = []


@app.get("/", response_class=HTMLResponse)
def index(request: Request, num: int = 0):
    ans = db["ans"]
    result = ""

    # -------Start of your code------------

    # This is an example.
    if num > max_num:
        result = f"1 ~ {max_num}"

    # -------End of your code-------------

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": result,
            "max_num": max_num,
            "num": num,
            "comments": list(db["comments"]),
        },
    )


@app.get("/hello-text")
def hello_text():
    return "hi i am text"


@app.get("/hello-query")  # GET /hello-query?query_a=xxx&query_b=xxx
def hello_query(query_a, query_b):
    return "query"


@app.get("/hello-html", response_class=HTMLResponse)
def hello_html(request: Request):
    return templates.TemplateResponse(
        "another.html",
        {
            "request": request,
        },
    )


# @app.get("/list")
# def get_list():
#     return [1, 2, 3, 4]


#
class Comment(BaseModel):
    id: str
    author: str
    content: str
    created_at: str


@app.get("/comments")
def get_comments():
    return list(db["comments"])


@app.post("/comments")
def create_comment(author: str = Form(""), content: str = Form("")):

    new_comment = {
        "id": str(random.randint(1, 99999999999)),
        "author": author,
        "content": content,
        "created_at": datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S"),
    }

    old_comments = list(db["comments"])

    comments = [new_comment] + old_comments
    db["comments"] = comments

    return new_comment


# comments
@app.delete("/comments")
def delete_comments():
    # Danger!! Only use it if you know what you're doing.
    # db["comments"] = []
    return "success"


'''
old_comments = list(db["comments"])
[
  comment1,
  comment2,
  comment3,
]

[
  {
    "id": str(random.randint(1, 99999999999)),
    "author": author,
    "content": content,
    "created_at": datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S"),
  }, 
  {
    "id": str(random.randint(1, 99999999999)),
    "author": author,
    "content": content,
    "created_at": datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S"),
  }

]
'''


# comment
@app.delete("/comments/{id}")  # ex: /comments/9527
def delete_comment(id: str):

    return "Message" + id


uvicorn.run(app, host="0.0.0.0", port="8080")
