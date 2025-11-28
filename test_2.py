#!/usr/bin/env python3
"""
A full-featured Task Manager CLI application.
Stores tasks in a JSON database and supports:
- Add task
- List tasks
- Complete task
- Delete task
- Search tasks
- Filter by status
"""

import json
import os
import sys
from datetime import datetime
from typing import List, Dict

DB_FILE = "tasks.json"


# ==========================
# Utilities
# ==========================
def load_db() -> List[Dict]:
    """Load task database."""
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_db(tasks: List[Dict]):
    """Save task database."""
    with open(DB_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def colored(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"


def green(text): return colored(text, "92")
def red(text): return colored(text, "91")
def yellow(text): return colored(text, "93")
def cyan(text): return colored(text, "96")


# ==========================
# Task Helpers
# ==========================
def add_task(description: str):
    tasks = load_db()
    new_task = {
        "id": len(tasks) + 1,
        "description": description,
        "completed": False,
        "created_at": datetime.now().isoformat()
    }
    tasks.append(new_task)
    save_db(tasks)
    print(green(f"Task added: {description}"))


def list_tasks(show_all=True, show_completed=None):
    tasks = load_db()

    if show_completed is not None:
        tasks = [t for t in tasks if t["completed"] == show_completed]

    if not tasks:
        print(yellow("No tasks found."))
        return

    for t in tasks:
        status = green("✔ Completed") if t["completed"] else red("✗ Pending")
        print(cyan(f"[{t['id']}] ") + f"{t['description']} - {status}")


def complete_task(task_id: int):
    tasks = load_db()
    for t in tasks:
        if t["id"] == task_id:
            t["completed"] = True
            save_db(tasks)
            print(green(f"Task {task_id} marked as completed."))
            return
    print(red(f"No task found with id {task_id}"))


def delete_task(task_id: int):
    tasks = load_db()
    filtered = [t for t in tasks if t["id"] != task_id]

    if len(filtered) == len(tasks):
        print(red(f"No task found with id {task_id}"))
        return

    save_db(filtered)
    print(yellow(f"Task {task_id} deleted."))


def search_tasks(keyword: str):
    tasks = load_db()
    matches = [t for t in tasks if keyword.lower() in t["description"].lower()]

    if not matches:
        print(yellow("No matching tasks found."))
        return

    print(green(f"Found {len(matches)} matching tasks:"))
    for t in matches:
        status = green("✔") if t["completed"] else red("✗")
        print(f"{cyan(f'[{t['id']}]')} {t['description']} - {status}")


# ==========================
# Command Line Interface
# ==========================
def print_help():
    print("""
Task Manager CLI
------------------------

Usage:
  python task_manager.py add "task description"
  python task_manager.py list
  python task_manager.py list --completed
  python task_manager.py list --pending
  python task_manager.py complete <task_id>
  python task_manager.py delete <task_id>
  python task_manager.py search <keyword>
  python task_manager.py help
""")


def main():
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print(red("Please provide a task description."))
        else:
            desc = " ".join(sys.argv[2:])
            add_task(desc)

    elif command == "list":
        if "--completed" in sys.argv:
            list_tasks(show_completed=True)
        elif "--pending" in sys.argv:
            list_tasks(show_completed=False)
        else:
            list_tasks()

    elif command == "complete":
        if len(sys.argv) < 3:
            print(red("Provide task ID."))
        else:
            complete_task(int(sys.argv[2]))

    elif command == "delete":
        if len(sys.argv) < 3:
            print(red("Provide task ID."))
        else:
            delete_task(int(sys.argv[2]))

    elif command == "search":
        if len(sys.argv) < 3:
            print(red("Provide search keyword."))
        else:
            keyword = " ".join(sys.argv[2:])
            search_tasks(keyword)

    elif command == "help":
        print_help()

    else:
        print(red("Unknown command."))
        print_help()


if __name__ == "__main__":
    main()
