# Final-Assignment
# Command Line Task Management App

#### Video Demo: https://youtu.be/Rnm6Zfrz_gI

## Project Overview

This project is a command line-based task management application developed using Python. It manages task data using the local file system without relying on external APIs. Users can access basic task management functions including adding tasks, listing tasks, editing, marking as complete, and deleting tasks.

## Features

- Add tasks (with title, priority, and deadline options)
- Display task lists (with various filtering options)
- Mark tasks as complete
- Delete tasks
- Export tasks to CSV files
- Import tasks from CSV files
- Display task statistics (completion rate, number of tasks by priority, etc.)


## File Structure

- `project.py`: Main program file implementing command line argument processing and various task management functions.
- `test_project.py`: File for testing each function in the project. Runs automated tests using pytest.
- `requirements.txt`: List of Python libraries required for the project.
- `README.md`: File containing project description and usage instructions (this file).
- `tasks.json`: JSON file where the application stores generated task data.

## Implementation Details

### project.py

This file contains the following main functions:

1. `main()`:  Program entry point. Parses command line arguments and calls appropriate functions.
2. `add_task(title, priority, due_date)`: Adds a new task with the specified title, priority, and deadline.
3. `list_tasks(show_all, priority_filter, due_days)`: Displays task list. Filtering options can be specified.
4. `complete_task(task_id)`: Marks the task with the specified ID as complete.
5. `delete_task(task_id)`: Deletes the task with the specified ID.
6. `export_tasks(filename)`: Exports tasks to a CSV file.
7. `import_tasks(filename)`: Imports tasks from a CSV file.
8. `show_stats()`: Displays task statistics.
9. `load_tasks()` and `save_tasks(tasks)`: Loads and saves task data from/to JSON file.

### Design Choices

- **Data Storage Format**: JSON was chosen because it works well with Python and allows for easy handling of structured data. It also stores data in a human-readable format.
- **Command Line Interface**: Implemented a subcommand-style interface using argparse. This allows for intuitive operation with a git-like command system.
- **Modularity性**: Each feature is implemented as an independent function, making testing and maintenance easier.
- **Filtering Options**: Multiple filtering options are provided for task list display, allowing users to quickly find necessary tasks even when there are many tasks.

## Usage

### Installation

```
pip install -r requirements.txt
```

### Basic Commands

#### Adding Tasks

```
python project.py add "Write report" --priority high --due 2023-12-31
```

Or in short form:

```
python project.py add "Buy milk" -p low -d 2023-12-25
```

#### Displaying Task List

All tasks (only incomplete ones):

```
python project.py list
```

All tasks (including completed ones):

```
python project.py list --all
```

Filtering by priority:

```
python project.py list --priority high
```

Filtering by deadline (tasks due within 7 days):

```
python project.py list --due 7
```

#### Marking Tasks as Complete

```
python project.py complete 1
```

#### Deleting Tasks

```
python project.py delete 2
```

#### Exporting Tasks

```
python project.py export tasks_backup.csv
```

#### Importing Tasks

```
python project.py import tasks_backup.csv
```

#### Displaying Statistics

```
python project.py stats
```

## Development Challenges

One of the main challenges faced when developing this project was designing the command line interface.
