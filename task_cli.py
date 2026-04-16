#!/usr/bin/env python3
"""
task-cli: A simple CLI task tracker that stores tasks in a JSON file.
Usage: python task_cli.py <command> [arguments]
"""

import sys
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"


# ── File helpers ──────────────────────────────────────────────────────────────

def load_tasks():
    """Load tasks from the JSON file, creating it if it doesn't exist."""
    if not os.path.exists(TASKS_FILE):
        save_tasks([])
        return []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return json.loads(content) if content else []
    except json.JSONDecodeError:
        print(f"Error: '{TASKS_FILE}' contains invalid JSON. Starting fresh.")
        return []


def save_tasks(tasks):
    """Persist tasks list to the JSON file."""
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


# ── Core commands ─────────────────────────────────────────────────────────────

def cmd_add(args):
    if not args:
        print("Error: 'add' requires a task description.")
        print("  Usage: task-cli add \"<description>\"")
        sys.exit(1)

    description = args[0]
    tasks = load_tasks()

    new_id = max((t["id"] for t in tasks), default=0) + 1
    now = datetime.now().isoformat(timespec="seconds")

    task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now,
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_id})")


def cmd_update(args):
    if len(args) < 2:
        print("Error: 'update' requires a task ID and a new description.")
        print("  Usage: task-cli update <id> \"<new description>\"")
        sys.exit(1)

    task_id, description = _parse_id(args[0], "update"), args[1]
    tasks = load_tasks()
    task = _find_task(tasks, task_id)

    task["description"] = description
    task["updatedAt"] = datetime.now().isoformat(timespec="seconds")
    save_tasks(tasks)
    print(f"Task {task_id} updated successfully.")


def cmd_delete(args):
    if not args:
        print("Error: 'delete' requires a task ID.")
        print("  Usage: task-cli delete <id>")
        sys.exit(1)

    task_id = _parse_id(args[0], "delete")
    tasks = load_tasks()
    _find_task(tasks, task_id)  # validate existence

    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    print(f"Task {task_id} deleted successfully.")


def cmd_mark(args, status):
    if not args:
        cmd_name = "mark-in-progress" if status == "in-progress" else "mark-done"
        print(f"Error: '{cmd_name}' requires a task ID.")
        print(f"  Usage: task-cli {cmd_name} <id>")
        sys.exit(1)

    task_id = _parse_id(args[0], f"mark-{status}")
    tasks = load_tasks()
    task = _find_task(tasks, task_id)

    task["status"] = status
    task["updatedAt"] = datetime.now().isoformat(timespec="seconds")
    save_tasks(tasks)
    print(f"Task {task_id} marked as '{status}'.")


def cmd_list(args):
    status_filter = args[0] if args else None

    valid_filters = {"todo", "in-progress", "done"}
    if status_filter and status_filter not in valid_filters:
        print(f"Error: Unknown status filter '{status_filter}'.")
        print(f"  Valid options: {', '.join(sorted(valid_filters))}")
        sys.exit(1)

    tasks = load_tasks()
    filtered = [t for t in tasks if not status_filter or t["status"] == status_filter]

    if not filtered:
        msg = "No tasks found."
        if status_filter:
            msg = f"No tasks with status '{status_filter}'."
        print(msg)
        return

    # Column widths
    id_w   = max(len(str(t["id"]))          for t in filtered)
    stat_w = max(len(t["status"])           for t in filtered)
    desc_w = max(len(t["description"])      for t in filtered)
    id_w, stat_w, desc_w = max(id_w, 2), max(stat_w, 6), max(desc_w, 11)

    header = (
        f"{'ID':<{id_w}}  {'STATUS':<{stat_w}}  {'DESCRIPTION':<{desc_w}}  "
        f"{'CREATED':<19}  {'UPDATED':<19}"
    )
    sep = "-" * len(header)

    print(sep)
    print(header)
    print(sep)
    for t in filtered:
        print(
            f"{t['id']:<{id_w}}  {t['status']:<{stat_w}}  "
            f"{t['description']:<{desc_w}}  "
            f"{t['createdAt']:<19}  {t['updatedAt']:<19}"
        )
    print(sep)
    print(f"{len(filtered)} task(s) shown.")


# ── Helpers ───────────────────────────────────────────────────────────────────

def _parse_id(value, cmd):
    try:
        task_id = int(value)
        if task_id <= 0:
            raise ValueError
        return task_id
    except ValueError:
        print(f"Error: '{value}' is not a valid task ID. IDs must be positive integers.")
        sys.exit(1)


def _find_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    print(f"Error: Task with ID {task_id} not found.")
    sys.exit(1)


# ── Entry point ───────────────────────────────────────────────────────────────

USAGE = """
task-cli — Simple command-line task tracker
-------------------------------------------
Commands:
  add "<description>"          Add a new task
  update <id> "<description>"  Update a task's description
  delete <id>                  Delete a task
  mark-in-progress <id>        Mark a task as in-progress
  mark-done <id>               Mark a task as done
  list                         List all tasks
  list todo                    List tasks with status 'todo'
  list in-progress             List tasks with status 'in-progress'
  list done                    List tasks with status 'done'
""".strip()


COMMANDS = {
    "add":              lambda args: cmd_add(args),
    "update":           lambda args: cmd_update(args),
    "delete":           lambda args: cmd_delete(args),
    "mark-in-progress": lambda args: cmd_mark(args, "in-progress"),
    "mark-done":        lambda args: cmd_mark(args, "done"),
    "list":             lambda args: cmd_list(args),
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print(USAGE)
        sys.exit(0)

    command = sys.argv[1]
    args    = sys.argv[2:]

    if command not in COMMANDS:
        print(f"Error: Unknown command '{command}'.")
        print()
        print(USAGE)
        sys.exit(1)

    COMMANDS[command](args)


if __name__ == "__main__":
    main()
