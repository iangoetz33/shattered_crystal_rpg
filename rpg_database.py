from tinydb import TinyDB, Query

# TinyDB creates this JSON file automatically if it does not exist.
DATABASE = TinyDB("rpg_save.json")
USERS = DATABASE.table("users")


def get_user(username):
    search = Query()
    return USERS.get(search.username == username)


def create_user(username, password_hash):
    USERS.insert({
        "username": username,
        "password_hash": password_hash,
        "progress": {},
    })


def save_player(username, progress):
    search = Query()
    USERS.update(
        {"progress": progress},
        search.username == username
    )
