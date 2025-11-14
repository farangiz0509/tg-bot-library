import json
import os
from typing import Optional

FILE = "users.json"


if not os.path.exists(FILE):
    with open(FILE, "w") as f:
        json.dump({}, f, indent=4)

def get_users() -> dict:
    with open(FILE, "r") as f:
        return json.load(f)

def save_users(users: dict):
    with open(FILE, "w") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

def add_or_update_user(tg_id: int, full_name: str, username: Optional[str] = None, lang: str = "uz"):
    users = get_users()
    key = str(tg_id)
    changed = False

    if key not in users:
        users[key] = {"full_name": full_name, "username": username, "lang": lang}
        changed = True
    else:
        
        if users[key].get("full_name") != full_name:
            users[key]["full_name"] = full_name
            changed = True
        if users[key].get("username") != username:
            users[key]["username"] = username
            changed = True
        if users[key].get("lang") != lang:
            users[key]["lang"] = lang
            changed = True

    if changed:
        save_users(users)

def get_user_lang(tg_id: int) -> str:
    users = get_users()
    return users.get(str(tg_id), {}).get("lang", "uz")

def set_user_lang(tg_id: int, lang: str):
    users = get_users()
    key = str(tg_id)
    if key not in users:
        users[key] = {"full_name": None, "username": None, "lang": lang}
    else:
        users[key]["lang"] = lang
    save_users(users)
