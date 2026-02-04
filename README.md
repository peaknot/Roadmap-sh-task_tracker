Hello! This is my very first beginner project.

# Task Tracker CLI

## Features
  - Add, update, and delete tasks
  - Mark tasks as done or in progress

  **List tasks by status:**
  - all
  - done
  - progress
  - todo (not started)

Tasks are stored in a JSON file (saved_tasks.json)

Includes automated tests using unittest

## Requirements
  - Python 3.10+ (uses match statements)
  - No external dependencies
  - Installation
  - Clone/download this project folder
  - Open a terminal in the project directory

## Usage
  **Run commands using:**

  - python main.py <command> [arguments]
  
  - *Add a task*
    
      - python main.py add "Buy milk."
  
  - *Delete a task*
    
      - python main.py delete 3

  - *Mark as in progress:*

      - python main.py update 2 progress

  - *List tasks*

      - python main.py list
      
      or
      
      - python main.py list all


  - *List completed tasks:*

      - python main.py list done


  - *List tasks in progress:*

      - python main.py list progress


  - *List tasks not started yet:*

      - python main.py list todo

## Output Format

**Tasks are displayed like:**

    [✅] 1. Task title -- (Updated: 01-21 Wednesday 17:23:17.132824)
    
    [⏳] 2. Another task -- (Updated: 01-21 Wednesday 17:25:10.004201)
    
    [ ]  3. Not started -- (Updated: 01-21 Wednesday 17:26:00.000120)


**Legend:**

    ✅ Done
    
    ⏳ In progress
    
    (blank) Todo / Not started

## Running Tests

  **Run all tests:**

    python -m unittest -v
    
    
  Run a specific test file:
    
    python -m unittest -v test_task_manager.py

### Project URL
        https://roadmap.sh/projects/task-tracker
