import hashlib
from getpass import getpass
from colorama import Fore
from rpg_database import get_user, create_user


def hash_password(password):
    # Store a hash instead of storing the password as readable text.
    return hashlib.sha256(password.encode()).hexdigest()


def register_or_login():
    while True:
        choice = input("Register a new account or log in? (register/login): ")
        choice = choice.strip().lower()

        if choice in ("register", "login"):
            break

        print("Please type register or login.")

    while True:
        username = input("Username: ").strip()
        if not username:
            print("Username cannot be empty.")
            continue

        password = getpass("Password: ")
        if not password:
            print("Password cannot be empty.")
            continue

        saved_user = get_user(username)

        if choice == "register":
            if saved_user:
                print("That username already exists. Choose login instead.")
                continue

            create_user(username, hash_password(password))
            print(Fore.GREEN + "Account created!")
            return username, {}

        if saved_user and saved_user["password_hash"] == hash_password(password):
            print(Fore.GREEN + "Login successful!")
            return username, saved_user.get("progress", {})

        print(Fore.RED + "Incorrect username or password. Try again.")
