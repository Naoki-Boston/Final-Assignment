# project.py
import argparse
import csv
import os
import json
from datetime import datetime, timedelta

# File to save task data
TASKS_FILE = "tasks.json"

def main():
    """
    Main function: Parse command-line arguments and call the appropriate function
    """
    parser = argparse.ArgumentParser(description="Simple task management application")
    subparsers = parser.add_subparsers(dest="command", help="command")
    
    # Subcommand to add a task
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("--priority", "-p", choices=["high", "medium", "low"], default="medium", help="Task priority")
    add_parser.add_argument("--due", "-d", help="Due date (YYYY-MM-DD format)")
    
    # Subcommand to list tasks
    list_parser = subparsers.add_parser("list", help="Display task list")
    list_parser.add_argument("--all", "-a", action="store_true", help="Display all tasks including completed ones")
    list_parser.add_argument("--priority", "-p", choices=["high", "medium", "low"], help="Display only tasks with the specified priority")
    list_parser.add_argument("--due", "-d", help="Display only tasks due within the specified number of days")
    
    # Subcommand to mark a task as complete
    complete_parser = subparsers.add_parser("complete", help="Mark a task as complete")
    complete_parser.add_argument("task_id", type=int, help="ID of the task to mark as complete")
    
    # Subcommand to delete a task
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", type=int, help="ID of the task to delete")
    
    # Subcommand to export tasks
    export_parser = subparsers.add_parser("export", help="Export tasks to a CSV file")
    export_parser.add_argument("filename", help="Name of the CSV file to export to")
    
    # Subcommand to import tasks
    import_parser = subparsers.add_parser("import", help="Import tasks from a CSV file")
    import_parser.add_argument("filename", help="Name of the CSV file to import from")
    
    # Subcommand to show statistics
    subparsers.add_parser("stats", help="Display task statistics")
    
    args = parser.parse_args()
    
    # Call the appropriate function based on the command
    if args.command == "add":
        add_task(args.title, args.priority, args.due)
        print(f"Task '{args.title}' has been added.")
    
    elif args.command == "list":
        list_tasks(args.all, args.priority, args.due)
    
    elif args.command == "complete":
        if complete_task(args.task_id):
            print(f"Task ID {args.task_id} has been marked as complete.")
        else:
            print(f"Task ID {args.task_id} was not found.")
    
    elif args.command == "delete":
        if delete_task(args.task_id):
            print(f"Task ID {args.task_id} has been deleted.")
        else:
            print(f"Task ID {args.task_id} was not found.")
    
    elif args.command == "export":
        export_tasks(args.filename)
        print(f"Tasks have been exported to {args.filename}.")
    
    elif args.command == "import":
        count = import_tasks(args.filename)
        print(f"{count} tasks have been imported from {args.filename}.")
    
    elif args.command == "stats":
        show_stats()
    
    else:
        # Display usage if no command is specified
        parser.print_help()

def add_task(title, priority="medium", due_date=None):
    """
    Add a new task
    
    Args:
        title (str): Task title
        priority (str): Task priority (high, medium, low)
        due_date (str): Due date (YYYY-MM-DD format)
        
    Returns:
        dict: The added task
    """
    tasks = load_tasks()
    
    # Determine the next task ID
    task_id = 1
    if tasks:
        task_id = max(task["id"] for task in tasks) + 1
    
    # Create a new task
    new_task = {
        "id": task_id,
        "title": title,
        "priority": priority,
        "due_date": due_date,
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Add to the task list and save
    tasks.append(new_task)
    save_tasks(tasks)
    
    return new_task

def list_tasks(show_all=False, priority_filter=None, due_days=None):
    """
    Display the task list
    
    Args:
        show_all (bool): Whether to display completed tasks as well
        priority_filter (str): Display only tasks with the specified priority
        due_days (str): Display only tasks due within the specified number of days
    """
    tasks = load_tasks()
    filtered_tasks = []
    
    # Current date
    today = datetime.now().date()
    
    for task in tasks:
        # Filter completed tasks
        if not show_all and task["completed"]:
            continue
            
        # Filter by priority
        if priority_filter and task["priority"] != priority_filter:
            continue
            
        # Filter by due date
        if due_days:
            # Skip tasks with no due date
            if not task["due_date"]:
                continue
                
            task_due = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
            days_left = (task_due - today).days
            
            if days_left < 0 or days_left > int(due_days):
                continue
                
        filtered_tasks.append(task)
    
    if not filtered_tasks:
        print("There are no tasks to display.")
        return
    
    # Display tasks
    print("\nID  | Priority | Due Date    | Status   | Title")
    print("-" * 60)
    
    for task in filtered_tasks:
        status = "Completed" if task["completed"] else "Incomplete"
        due_str = task["due_date"] if task["due_date"] else "None"
        
        print(f"{task['id']:<4}| {task['priority']:<6} | {due_str:<11} | {status:<10} | {task['title']}")
    
    print()
    
    return filtered_tasks

def complete_task(task_id):
    """
    Mark the task with the specified ID as complete
    
    Args:
        task_id (int): ID of the task to mark as complete
        
    Returns:
        bool: Whether the task was found and marked as complete
    """
    tasks = load_tasks()
    
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_tasks(tasks)
            return True
    
    return False

def delete_task(task_id):
    """
    Delete the task with the specified ID
    
    Args:
        task_id (int): ID of the task to delete
        
    Returns:
        bool: Whether the task was found and deleted
    """
    tasks = load_tasks()
    
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            del tasks[i]
            save_tasks(tasks)
            return True
    
    return False

def export_tasks(filename):
    """
    Export tasks to a CSV file
    
    Args:
        filename (str): Name of the CSV file to export to
    """
    tasks = load_tasks()
    
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["id", "title", "priority", "due_date", "completed", "created_at", "completed_at"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for task in tasks:
            writer.writerow(task)

def import_tasks(filename):
    """
    Import tasks from a CSV file
    
    Args:
        filename (str): Name of the CSV file to import from
        
    Returns:
        int: Number of tasks imported
    """
    tasks = load_tasks()
    imported_count = 0
    
    with open(filename, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Determine the next task ID
        next_id = 1
        if tasks:
            next_id = max(task["id"] for task in tasks) + 1
        
        for row in reader:
            # Assign a new ID to avoid duplicates with existing tasks
            new_task = {
                "id": next_id,
                "title": row["title"],
                "priority": row["priority"],
                "due_date": row["due_date"] if row["due_date"] else None,
                "completed": row["completed"].lower() == "true",
                "created_at": row["created_at"] if "created_at" in row else datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "completed_at": row["completed_at"] if "completed_at" in row and row["completed_at"] else None
            }
            
            tasks.append(new_task)
            next_id += 1
            imported_count += 1
    
    save_tasks(tasks)
    return imported_count

def show_stats():
    """Display task statistics"""
    tasks = load_tasks()
    
    if not tasks:
        print("There are no tasks.")
        return
    
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task["completed"])
    completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    
    # Number of tasks by priority
    priority_counts = {"high": 0, "medium": 0, "low": 0}
    for task in tasks:
        priority_counts[task["priority"]] += 1
    
    # Number of overdue tasks
    today = datetime.now().date()
    overdue_tasks = 0
    for task in tasks:
        if not task["completed"] and task["due_date"]:
            task_due = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
            if task_due < today:
                overdue_tasks += 1
    
    # Display statistics
    print("\n===== Task Statistics =====")
    print(f"Total tasks: {total_tasks}")
    print(f"Completed tasks: {completed_tasks}")
    print(f"Completion rate: {completion_rate:.1f}%")
    print("\nTasks by priority:")
    for priority, count in priority_counts.items():
        print(f"  {priority}: {count}")
    print(f"\nOverdue tasks: {overdue_tasks}")
    
    if completed_tasks > 0:
        # Calculate average task completion time
        completion_times = []
        for task in tasks:
            if task["completed"] and "completed_at" in task:
                created = datetime.strptime(task["created_at"], "%Y-%m-%d %H:%M:%S")
                completed = datetime.strptime(task["completed_at"], "%Y-%m-%d %H:%M:%S")
                completion_times.append((completed - created).total_seconds() / 3600)  # in hours
        
        if completion_times:
            avg_completion_time = sum(completion_times) / len(completion_times)
            print(f"\nAverage task completion time: {avg_completion_time:.1f} hours")

def load_tasks():
    """
    Load task data from file
    
    Returns:
        list: List of tasks
    """
    if not os.path.exists(TASKS_FILE):
        return []
    
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    """
    Save task data to file
    
    Args:
        tasks (list): List of tasks to save
    """
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()