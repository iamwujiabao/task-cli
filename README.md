# task-cli

A lightweight command-line task tracker written in pure Python (no external dependencies). Tasks are stored in a local `tasks.json` file.

---

## Requirements

- Python 3.6+
- No third-party libraries needed

---

## Setup

```bash
# Clone / copy task_cli.py into your project directory, then:
chmod +x task_cli.py          # make it executable (macOS / Linux)

# Optional: create a convenient alias
alias task-cli="python3 /path/to/task_cli.py"
```

On Windows, run with:
```cmd
python task_cli.py <command> [arguments]
```

---

## Usage

```
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
```

---

## Examples

```bash
# Add tasks
python task_cli.py add "Buy groceries"
# Task added successfully (ID: 1)

python task_cli.py add "Walk the dog"
# Task added successfully (ID: 2)

python task_cli.py add "Read a book"
# Task added successfully (ID: 3)

# Update a task
python task_cli.py update 1 "Buy groceries and cook dinner"

# Mark tasks
python task_cli.py mark-in-progress 1
python task_cli.py mark-done 2

# List all tasks
python task_cli.py list

# List by status
python task_cli.py list todo
python task_cli.py list in-progress
python task_cli.py list done

# Delete a task
python task_cli.py delete 3
```

---

## Data Storage

Tasks are saved to **`tasks.json`** in the current working directory. The file is created automatically on first use.

Each task has the following fields:

| Field         | Type   | Description                        |
|---------------|--------|------------------------------------|
| `id`          | int    | Unique auto-incrementing identifier |
| `description` | string | Task description                   |
| `status`      | string | `todo`, `in-progress`, or `done`   |
| `createdAt`   | string | ISO-8601 timestamp of creation     |
| `updatedAt`   | string | ISO-8601 timestamp of last update  |

Example `tasks.json`:

```json
[
  {
    "id": 1,
    "description": "Buy groceries and cook dinner",
    "status": "in-progress",
    "createdAt": "2025-04-15T09:00:00",
    "updatedAt": "2025-04-15T10:30:00"
  }
]
```

---

## Error Handling

The CLI handles common error cases gracefully:

- Invalid or non-existent task ID → prints a clear error message
- Missing required arguments → prints usage hint
- Corrupt `tasks.json` → warns and starts fresh
- Unknown commands → prints full usage guide
