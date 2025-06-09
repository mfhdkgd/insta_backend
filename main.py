from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from fastapi import FastAPI, Form
from utils import login_and_save_session, like_and_comment_on_posts

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.post("/login/")
def login(
    username: str = Form(...),
    password: str = Form(...),
    code: str = Form(None)  # برای کد ۲FA (اختیاری)
):
    result = login_and_save_session(username, password, verification_code=code)
    return result
    

@app.post("/like_comment/")
def do_actions(username: str = Form(...)):
    result = like_and_comment_on_posts(username)
    return result
    
    
@app.get("/", response_class=HTMLResponse)
async def show_panel(request: Request):
    return templates.TemplateResponse("panel.html", {"request": request})
