from instagrapi import Client
from instagrapi.exceptions import TwoFactorRequired
import os
import pickle
import time
import random

SESSION_FOLDER = "sessions"

def login_and_save_session(username, password, verification_code=None):
    cl = Client()
    session_path = f"{SESSION_FOLDER}/{username}_session.pkl"

    if os.path.exists(session_path):
        with open(session_path, "rb") as f:
            cl = pickle.load(f)
        try:
            cl.get_timeline_feed()
            return {"success": True, "message": "Session loaded"}
        except:
            os.remove(session_path)

    try:
        if verification_code:
            cl.login(username, password, verification_code=verification_code)
        else:
            cl.login(username, password)
    except TwoFactorRequired:
        return {"success": False, "message": "2FA required"}

    with open(session_path, "wb") as f:
        pickle.dump(cl, f)

    return {"success": True, "message": "Login successful and session saved."}


def like_and_comment_on_posts(username):
    session_path = f"{SESSION_FOLDER}/{username}_session.pkl"

    if not os.path.exists(session_path):
        return {"success": False, "message": "Session not found. Please login first."}

    with open(session_path, "rb") as f:
        cl = pickle.load(f)

    try:
        cl.get_timeline_feed()
    except Exception as e:
        return {"success": False, "message": f"Session invalid: {e}"}

    target_usernames = ["iranbetnet"]  # لیست پیج‌ها
    amount = 10
    total_done = 0

    for username in target_usernames:
        try:
            user_id = cl.user_id_from_username(username)
            posts = cl.user_medias(user_id, amount)
        except Exception as e:
            continue

        for post in posts:
            action = random.choice(["like", "comment", "both"])

            if action in ["like", "both"]:
                try:
                    cl.media_like(post.id)
                except:
                    pass

            if action in ["comment", "both"]:
                time.sleep(random.randint(10, 30))
                try:
                    comment = random.choice([
                        "Nice shot! 🔥",
                        "Great post! 💯",
                        "Awesome picture 🙌",
                        "Loved this! 🌿",
                        "Wow! 📸"
                    ])
                    cl.media_comment(post.id, comment)
                except:
                    pass

            time.sleep(random.randint(30, 60))
            total_done += 1

    return {"success": True, "message": f"Done for {total_done} posts."}
