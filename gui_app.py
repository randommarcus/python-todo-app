import tkinter as tk
from tkinter import messagebox
from todo_app import Task, load_tasks_from_file, save_tasks_to_file, MOCK_SUGGESTIONS
import datetime
import random # NEW: Import random for suggestions

class TodoAppGUI:
    def __init__(self, root):
        """Initializes the GUI application."""
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("650x600") # Increased height for new buttons

        # Backend Integration
        self.filename = "tasks.json"
        self.tasks = load_tasks_from_file(self.filename)

        # Input Frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)
        
        self.task_label = tk.Label(input_frame, text="Task:", font=("Helvetica", 12))
        self.task_label.pack(side=tk.LEFT, padx=(10,5))
        self.task_entry = tk.Entry(input_frame, width=30, font=("Helvetica", 12))
        self.task_entry.pack(side=tk.LEFT)

        self.date_label = tk.Label(input_frame, text="Due Date (YYYY-MM-DD):", font=("Helvetica", 12))
        self.date_label.pack(side=tk.LEFT, padx=(10,5))
        self.date_entry = tk.Entry(input_frame, width=15, font=("Helvetica", 12))
        self.date_entry.pack(side=tk.LEFT)

        self.add_button = tk.Button(self.root, text="Add Task", font=("Helvetica", 11, "bold"), command=self.add_task_gui)
        self.add_button.pack(pady=5)

        # Listbox for tasks
        self.task_listbox = tk.Listbox(self.root, height=15, width=70, font=("Helvetica", 12), selectbackground="#a6a6a6")
        self.task_listbox.pack(pady=10)

        # Frame for main action buttons
        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=5)

        self.mark_complete_button = tk.Button(action_frame, text="Mark as Complete", font=("Helvetica", 11), command=self.mark_complete_gui)
        self.mark_complete_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = tk.Button(action_frame, text="Edit Selected", font=("Helvetica", 11), command=self.edit_task_gui)
        self.edit_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = tk.Button(action_frame, text="Delete Selected", font=("Helvetica", 11), command=self.delete_task_gui)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        # --- NEW: Frame for extra features ---
        extra_frame = tk.Frame(self.root)
        extra_frame.pack(pady=10)

        self.sort_button = tk.Button(extra_frame, text="Sort by Due Date", font=("Helvetica", 11), command=self.sort_tasks_gui)
        self.sort_button.pack(side=tk.LEFT, padx=5)

        self.suggest_button = tk.Button(extra_frame, text="Suggest a Task", font=("Helvetica", 11), command=self.suggest_task_gui)
        self.suggest_button.pack(side=tk.LEFT, padx=5)

        self.refresh_task_list()

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, str(task))

    def add_task_gui(self):
        task_description = self.task_entry.get()
        due_date_str = self.date_entry.get()
        if not task_description:
            messagebox.showwarning("Warning", "You must enter a task.")
            return
        if due_date_str:
            try:
                datetime.datetime.strptime(due_date_str, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Warning", "Invalid date format. Please use YYYY-MM-DD.")
                return
        else:
            due_date_str = None
        new_task = Task(description=task_description, due_date=due_date_str)
        self.tasks.append(new_task)
        save_tasks_to_file(self.tasks, self.filename)
        self.refresh_task_list()
        self.task_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)

    def mark_complete_gui(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            task = self.tasks[selected_task_index]
            task.mark_complete()
            save_tasks_to_file(self.tasks, self.filename)
            self.refresh_task_list()
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task.")

    def delete_task_gui(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
                self.tasks.pop(selected_task_index)
                save_tasks_to_file(self.tasks, self.filename)
                self.refresh_task_list()
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task.")

    def edit_task_gui(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            task = self.tasks[selected_task_index]
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Task")
            tk.Label(edit_window, text="Description:", font=("Helvetica", 12)).pack(pady=(10,0))
            desc_entry = tk.Entry(edit_window, width=40, font=("Helvetica", 12))
            desc_entry.pack(pady=5, padx=10)
            desc_entry.insert(0, task.description)
            tk.Label(edit_window, text="Due Date (YYYY-MM-DD):", font=("Helvetica", 12)).pack()
            date_entry = tk.Entry(edit_window, width=20, font=("Helvetica", 12))
            date_entry.pack(pady=5, padx=10)
            if task.due_date:
                date_entry.insert(0, task.due_date)
            save_button = tk.Button(edit_window, text="Save Changes", font=("Helvetica", 11, "bold"), 
                                    command=lambda: self.save_edited_task(task, desc_entry, date_entry, edit_window))
            save_button.pack(pady=10)
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to edit.")

    def save_edited_task(self, task, desc_entry, date_entry, edit_window):
        new_description = desc_entry.get()
        new_due_date = date_entry.get()
        if not new_description:
            messagebox.showwarning("Warning", "Description cannot be empty.", parent=edit_window)
            return
        if new_due_date:
            try:
                datetime.datetime.strptime(new_due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Warning", "Invalid date format.", parent=edit_window)
                return
        else:
            new_due_date = None
        task.description = new_description
        task.due_date = new_due_date
        save_tasks_to_file(self.tasks, self.filename)
        self.refresh_task_list()
        edit_window.destroy()

    # --- NEW: Methods for sorting and suggestions ---
    def sort_tasks_gui(self):
        """Sorts the tasks by due date and refreshes the list."""
        def sort_key(task):
            return task.due_date or '9999-12-31'
        # Replace the current task list with the sorted version
        self.tasks = sorted(self.tasks, key=sort_key)
        # Save the new order and update the screen
        save_tasks_to_file(self.tasks, self.filename)
        self.refresh_task_list()
        messagebox.showinfo("Success", "Tasks have been sorted by due date.")

    def suggest_task_gui(self):
        """Suggests a random task and asks the user to add it."""
        suggestion = random.choice(MOCK_SUGGESTIONS)
        # Use a GUI-friendly confirmation box
        if messagebox.askyesno("Task Suggestion", f"How about this?\n\n'{suggestion}'\n\nAdd it to your list?"):
            new_task = Task(description=suggestion)
            self.tasks.append(new_task)
            save_tasks_to_file(self.tasks, self.filename)
            self.refresh_task_list()

if __name__ == "__main__":
    # Make sure to also import MOCK_SUGGESTIONS from todo_app.py
    root = tk.Tk()
    app = TodoAppGUI(root)
    root.mainloop()