import tkinter as tk
from tkinter import messagebox
# NEW: Import the logic from your other file
from todo_app import Task, load_tasks_from_file, save_tasks_to_file

class TodoAppGUI:
    def __init__(self, root):
        """Initializes the GUI application."""
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("500x550")

        # --- NEW: Backend Integration ---
        self.filename = "tasks.json"
        self.tasks = load_tasks_from_file(self.filename)

        # --- Create Widgets ---
        
        # Frame for input widgets
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        # Label and Entry for new tasks
        self.task_label = tk.Label(input_frame, text="New Task:", font=("Helvetica", 12))
        self.task_label.pack(side=tk.LEFT, padx=5)
        self.task_entry = tk.Entry(input_frame, width=35, font=("Helvetica", 12))
        self.task_entry.pack(side=tk.LEFT)

        # 'Add Task' Button
        self.add_button = tk.Button(self.root, text="Add Task", font=("Helvetica", 11, "bold"), command=self.add_task_gui)
        self.add_button.pack(pady=5)

        # --- NEW: Listbox for displaying tasks ---
        self.task_listbox = tk.Listbox(self.root, height=15, width=60, font=("Helvetica", 12), selectbackground="#a6a6a6")
        self.task_listbox.pack(pady=10)

        # NEW: Initial population of the listbox
        self.refresh_task_list()

    def refresh_task_list(self):
        """Clears and re-populates the listbox with current tasks."""
        # NEW: This method keeps the on-screen list in sync with our task list
        self.task_listbox.delete(0, tk.END) # Clear the listbox
        for task in self.tasks:
            self.task_listbox.insert(tk.END, str(task)) # Insert the string representation of each task

    def add_task_gui(self):
        """GUI function to handle adding a new task."""
        task_description = self.task_entry.get()

        if task_description:
            # MODIFIED: Use our backend logic
            new_task = Task(description=task_description)
            self.tasks.append(new_task)
            save_tasks_to_file(self.tasks, self.filename)
            self.refresh_task_list() # Update the on-screen list
            self.task_entry.delete(0, tk.END) # Clear the entry box
        else:
            messagebox.showwarning("Warning", "You must enter a task.")

# --- Main execution block ---
if __name__ == "__main__":
    # Make sure both gui_app.py and todo_app.py are in the same folder
    root = tk.Tk()
    app = TodoAppGUI(root)
    root.mainloop()