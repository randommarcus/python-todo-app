import random
import requests
import datetime
import json

class Task:
    """Represents a single task in the to-do list."""
    def __init__(self, description, due_date=None, status='incomplete'):
        """Initializes a new Task object."""
        self.description = description
        self.status = status
        self.due_date = due_date

    def __str__(self):
        """Returns a user-friendly string representation of the task."""
        status_marker = "[x]" if self.status == 'complete' else "[ ]"
        due_date_str = f"(Due: {self.due_date})" if self.due_date else ""
        return f"{status_marker} {self.description} {due_date_str}".strip()

    def mark_complete(self):
        """Marks the task as complete."""
        self.status = 'complete'

    def to_dict(self):
        """Converts the Task object to a dictionary for JSON serialization."""
        return {
            "description": self.description,
            "status": self.status,
            "due_date": self.due_date
        }

print("Hello, To-Do List!")

# Initialize our list of tasks
tasks = []
FILENAME = "tasks.json" # Define the filename as a constant

# A list of mock suggestions to use if the API fails or is blocked.
MOCK_SUGGESTIONS = [
    "Learn a new programming language",
    "Organize your bookshelf",
    "Go for a 30-minute walk",
    "Write a short story or poem",
    "Try a new recipe",
    "Listen to a new album from start to finish",
    "Clean out your email inbox",
    "Watch a documentary on a topic you know nothing about"
]

def show_menu():
    """Displays the main menu to the user."""
    print("\n--- To-Do List Menu ---")
    print("1. Add a new task")
    print("2. View all tasks")
    print("3. View tasks sorted by due date")
    print("4. Mark a task as complete")
    print("5. Edit a task")
    print("6. Delete a task")
    print("7. Suggest a random task")
    print("8. Exit")

def load_tasks_from_file(filename):
    """Loads tasks from a JSON file and returns a list of Task objects."""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            # Create a Task object for each dictionary in the file
            return [Task(**task_data) for task_data in data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks_to_file(task_list, filename):
    """Saves a list of Task objects to a JSON file."""
    with open(filename, 'w') as f:
        # Convert each Task object to its dictionary representation
        json.dump([task.to_dict() for task in task_list], f, indent=4)

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
    
    # Create an instance of the Task class
    new_task = Task(description, due_date=due_date_str) # Simplified!
    task_list.append(new_task)
    print(f"Task '{description}' has been added.")


def view_tasks(task_list):
    """Displays all tasks with their status and due date."""
    print("\n--- Your To-Do List ---")
    if not task_list:
        print("Your to-do list is empty!")
    else:
        for index, task in enumerate(task_list):
            # Because of the __str__ method, we can just print the object!
            print(f"{index + 1}. {task}")

def edit_task(task_list):
    """Edits an existing task's description or due date."""
    view_tasks(task_list)

    if not task_list:
        return

    try:
        task_num = int(input("Enter the number of the task to edit: "))

        if 1 <= task_num <= len(task_list):
            task_index = task_num - 1
            # Get the actual Task object
            task = task_list[task_index]

            print(f"Editing task: {task.description}")
            print("What do you want to edit?")
            print("1. Description")
            print("2. Due Date")
            choice = input("Enter your choice (1-2): ")

            if choice == '1':
                new_description = input("Enter the new description: ")
                task.description = new_description # Set the attribute directly
                print("Description updated successfully!")
            elif choice == '2':
                new_due_date_str = input("Enter the new due date (YYYY-MM-DD): ")
                # You can reuse your date validation logic here
                try:
                    datetime.datetime.strptime(new_due_date_str, "%Y-%m-%d")
                    task.due_date = new_due_date_str # Set the attribute
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
    view_tasks(task_list)

    if not task_list:
        return

    try:
        task_num_to_delete = int(input("Enter the number of the task to delete: "))

        if 1 <= task_num_to_delete <= len(task_list):
            index_to_delete = task_num_to_delete - 1
            removed_task = task_list.pop(index_to_delete)
            # Access the description attribute from the removed object
            print(f"Task '{removed_task.description}' was successfully deleted.")
        else:
            print("Invalid task number. Please try again.")

    except ValueError:
        print("Invalid input. Please enter a number.")

def mark_task_complete(task_list):
    """Marks a task as complete by calling its method."""
    view_tasks(task_list) # Show tasks to choose from
    try:
        task_num = int(input("Enter the number of the task to mark as complete: "))
        if 1 <= task_num <= len(task_list):
            task = task_list[task_num - 1]
            # Call the method directly on the object
            task.mark_complete()
            print(f"Task '{task.description}' marked as complete.")
        # ... (rest of your error handling)
    except ValueError:
        print("Invalid input.")

def view_sorted_tasks(task_list):
    """Sorts tasks by due date and displays them."""
    print("\n--- Tasks Sorted by Due Date ---")

    # The sort key now accesses the object's attribute
    def sort_key(task):
        return task.due_date or '9999-12-31'

    sorted_list = sorted(task_list, key=sort_key)

    if not sorted_list:
        print("Your to-do list is empty!")
    else:
        for index, task in enumerate(sorted_list):
            # The __str__ method handles the formatting automatically
            print(f"{index + 1}. {task}")

def suggest_task(task_list):
    """Suggests a random task and creates a Task object if accepted."""
    print("\nGetting a task suggestion...")
    
    suggestion = random.choice(MOCK_SUGGESTIONS)

    print(f"Suggestion: {suggestion}")
    
    add_it = input("Do you want to add this to your to-do list? (yes/no): ").lower()
    
    if add_it == 'yes':
        # Instead of a dictionary, create an instance of the Task class
        new_task = Task(description=suggestion)
        
        task_list.append(new_task)
        print(f"'{suggestion}' has been added to your list.")
    else:
        print("Suggestion discarded.")

# Main application loop
while True:
    show_menu()
    choice = input("Enter your choice (1-8): ")

    if choice == '1':
        add_task(tasks)
        save_tasks_to_file(tasks, FILENAME) # Save after adding a task
    elif choice == '2':
        view_tasks(tasks)
    elif choice == '3':
        view_sorted_tasks(tasks)
    elif choice == '4':
        mark_task_complete(tasks)
        save_tasks_to_file(tasks, FILENAME) # Save changes after marking a task complete
    elif choice == '5':
            edit_task(tasks)
            save_tasks_to_file(tasks, FILENAME) # Save changes after editing
    elif choice == '6':
            delete_task(tasks)
            save_tasks_to_file(tasks, FILENAME) # Save changes after deleting
    elif choice == '7':
        suggest_task(tasks)
        save_tasks_to_file(tasks, FILENAME)
    elif choice == '8':
        print("Exiting the To-Do List App. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 4.")