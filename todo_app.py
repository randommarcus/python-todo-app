import datetime
import json

print("Hello, To-Do List!")

# Initialize our list of tasks
tasks = []
FILENAME = "tasks.json" # Define the filename as a constant

def show_menu():
    """Displays the main menu to the user."""
    print("\nWhat would you like to do?")
    print("1. Add a new task")
    print("2. View all tasks")
    print("3. Mark a task as complete")
    print("4. Edit a task")
    print("5. Delete a task")
    print("6. Exit")

def load_tasks_from_file(filename):
    """Loads tasks from a JSON file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return [] # Return empty list if file doesn't exist
    except json.JSONDecodeError:
        return [] # Return empty list if file is empty or corrupted

def save_tasks_to_file(task_list, filename):
    """Saves the task list to a JSON file."""
    with open(filename, 'w') as f:
        # `indent=4` makes the JSON file human-readable
        json.dump(task_list, f, indent=4)

def add_task(task_list):
    """Adds a new task with a due date to the list."""
    description = input("Enter the new task description: ")
    due_date_str = input("Enter the due date (YYYY-MM-DD), or leave blank for none: ")
    
    # Date validation
    due_date = None
    if due_date_str:
        try:
            # This line checks if the date is valid. It will raise a ValueError if not.
            datetime.datetime.strptime(due_date_str, "%Y-%m-%d")
            due_date = due_date_str
        except ValueError:
            print("Invalid date format. Task will be added without a due date.")
            due_date = None # Ensure it's reset if format is wrong
    
    new_task = {
        "description": description,
        "status": "incomplete",
        "due_date": due_date  # Can be the string or None
    }
    task_list.append(new_task)
    print(f"Task '{description}' has been added.")


def view_tasks(task_list):
    """Displays all tasks with their status and due date."""
    print("\n--- Your To-Do List ---")
    if not task_list:
        print("Your to-do list is empty!")
    else:
        for index, task in enumerate(task_list):
            status_marker = "[x]" if task['status'] == 'complete' else "[ ]"
            # Get the due date, display 'No due date' if it's None
            due_date = task.get('due_date', 'No due date')
            if due_date is None:
                due_date = 'No due date'

            print(f"{index + 1}. {status_marker} {task['description']} (Due: {due_date})")

def edit_task(task_list):
    """Edits an existing task's description or due date."""
    view_tasks(task_list)

    if not task_list:
        return

    try:
        task_num = int(input("Enter the number of the task to edit: "))

        if 1 <= task_num <= len(task_list):
            task_index = task_num - 1
            task = task_list[task_index]

            print(f"Editing task: {task['description']}")
            print("What do you want to edit?")
            print("1. Description")
            print("2. Due Date")
            choice = input("Enter your choice (1-2): ")

            if choice == '1':
                new_description = input("Enter the new description: ")
                task['description'] = new_description
                print("Description updated successfully!")
            elif choice == '2':
                new_due_date_str = input("Enter the new due date (YYYY-MM-DD): ")
                try:
                    datetime.datetime.strptime(new_due_date_str, "%Y-%m-%d")
                    task['due_date'] = new_due_date_str
                    print("Due date updated successfully!")
                except ValueError:
                    print("Invalid date format. Due date not changed.")
            else:
                print("Invalid choice.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def delete_task(task_list):
    """Deletes a task from the list."""
    view_tasks(task_list) # First, show the user the tasks with numbers

    if not task_list: # Don't ask for input if there are no tasks
        return

    try:
        # Ask the user for the number of the task they want to delete.
        task_num_to_delete = int(input("Enter the number of the task to delete: "))

        # Check if the number is valid
        if 1 <= task_num_to_delete <= len(task_list):
            # Adjust for 0-based index (user enters 1, we delete index 0)
            index_to_delete = task_num_to_delete - 1
            # list.pop(index) removes the item at the given index
            removed_task = task_list.pop(index_to_delete)
            removed_task_desc = removed_task['description']
            print(f"Task '{removed_task_desc}' was successfully deleted.")
        else:
            print("Invalid task number. Please try again.")

    except ValueError:
        # This block runs if the user enters something that can't be converted to an integer
        print("Invalid input. Please enter a number.")

def mark_task_complete(task_list):
    """Marks a task as complete."""
    view_tasks(task_list)

    if not task_list:
        return

    try:
        task_num = int(input("Enter the number of the task to mark as complete: "))
        if 1 <= task_num <= len(task_list):
            task_list[task_num - 1]['status'] = 'complete'
            description = task_list[task_num - 1]['description']
            print(f"Task '{description}' marked as complete.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Main application loop
while True:
    show_menu()
    choice = input("Enter your choice (1-6): ")

    if choice == '1':
        add_task(tasks)
        save_tasks_to_file(tasks, FILENAME) # Save after adding a task
    elif choice == '2':
        view_tasks(tasks)
    elif choice == '3':
        mark_task_complete(tasks)
        save_tasks_to_file(tasks, FILENAME) # Save changes after marking a task complete
    elif choice == '4':
            edit_task(tasks)
            save_tasks_to_file(tasks, FILENAME) # Save changes after editing
    elif choice == '5':
            delete_task(tasks)
            save_tasks_to_file(tasks, FILENAME) # Save changes after deleting
    elif choice == '6':
        print("Exiting the To-Do List App. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 4.")