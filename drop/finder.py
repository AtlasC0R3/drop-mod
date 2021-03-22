import os


def find_guilds():
    try:
        return os.listdir('data/servers/')
    except FileNotFoundError:
        return []


def find_todos():
    todo_files = []
    try:
        files = os.listdir("data/todo/")
    except FileNotFoundError:
        return todo_files
    for file in files:
        if file.endswith(".json"):
            todo_files.append(file.split('.')[0])
    return todo_files
