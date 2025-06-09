from fastapi import FastAPI, Form
from utils import login_and_save_session, like_and_comment_on_posts

app = FastAPI()

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
