# Command-Line Task Management App

#### Video Demo: https://youtu.be/Rnm6Zfrz_gI

## Project Background

In today's digital environment, efficient task management is key to improving productivity. This command-line task management application was developed as a solution that combines simplicity and flexibility. Designed as an alternative to complex GUI tools and expensive project management software, it aims to provide a quick and easy way to manage tasks directly from the terminal.

## Detailed Features

### 1. Comprehensive Task Management

#### Task Addition
- Detailed task information input
  - Title (required)
  - Priority (high, medium, low)
  - Due date
- Automatic unique task ID generation
- Automatic task creation timestamp recording

#### Task Listing
- Flexible filtering options
  - Priority-based display
  - Due date-based display
  - Complete/incomplete task toggling
- Clear tabular output
- Detailed task information display

#### Task Management
- Mark tasks as complete
- Task deletion
- Automatic completion timestamp recording

### 2. Data Management Features

#### Export/Import
- Task export to CSV files
  - Saving all task information
- Task import from CSV files
  - Avoiding duplicate tasks
  - ID reassignment

#### Data Persistence
- Local storage using JSON files
- Human-readable data format
- Safe data saving and loading

### 3. Analysis and Insights

#### Task Statistics
- Total number of tasks
- Completed tasks and completion rate
- Priority-based task distribution
- Overdue task tracking
- Average task completion time

## Installation Guide

### System Requirements

- **Operating Systems**: 
  - macOS 10.14+
  - Windows 10+
  - Linux (Ubuntu 18.04+, Fedora 30+)
- **Python**: Version 3.7 or higher
- **Required Permissions**: 
  - File read/write access
  - Python execution environment

### Installation Steps

1. Verify Python
```bash
python3 --version
```

2. Create Virtual Environment (Recommended)
```bash
python3 -m venv taskmanager-env
source taskmanager-env/bin/activate  # macOS/Linux
taskmanager-env\Scripts\activate     # Windows
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Detailed Usage

### Basic Commands

#### Adding Tasks
```bash
# Simple addition
python project.py add "Create shopping list"

# Specify priority and due date
python project.py add "Project report" --priority high --due 2024-03-15
```

#### Listing Tasks
```bash
# Default (incomplete tasks)
python project.py list

# All tasks
python project.py list --all

# Only high-priority tasks
python project.py list --priority high

# Tasks due within 7 days
python project.py list --due 7
```

#### Task Management
```bash
# Mark task as complete
python project.py complete 3

# Delete task
python project.py delete 2
```

#### Data Management
```bash
# Export tasks to CSV
python project.py export mytasks_backup.csv

# Import tasks from another CSV
python project.py import external_tasks.csv
```

#### Analysis
```bash
# Display task statistics
python project.py stats
```

## Advanced Usage Scenarios

### Scenario 1: Project Management
1. Add all project tasks
2. Filter by priority
3. Track deadlines
4. Regularly check statistics

### Scenario 2: Personal Task Management
- Quickly add daily tasks
- Focus on tasks approaching deadline
- Track completion rate

## Troubleshooting

### Common Issues and Solutions
- **JSON file corruption**: Delete `tasks.json` and restart the app
- **Import errors**: Verify CSV file format
- **Permission errors**: Ensure appropriate permissions

## Future Development Plans

- [ ] Recurring task support
- [ ] Reminder functionality
- [ ] Cloud synchronization option
- [ ] Tagging feature

## How to Contribute

1. Check Issues
2. Fork the repository
3. Create a new branch
4. Commit changes
5. Submit a pull request

## License

[Add appropriate open-source license (e.g., MIT)]

## Contact & Support

- Email: [your-email]
- GitHub Issues: [your-repository-url]

## Credits

- Development: [Your Name]
- Design: [Designer Name]
- Testing Collaboration: [Tester Names]
