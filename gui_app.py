import tkinter as tk
from tkinter import messagebox

class TodoAppGUI:
    def __init__(self, root):
        """Initializes the GUI application."""
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("400x500") # Set window size

        # --- Create Widgets ---
        
        # Frame for input widgets
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        # Label for the entry box
        self.task_label = tk.Label(input_frame, text="New Task:", font=("Helvetica", 12))
        self.task_label.pack(side=tk.LEFT, padx=5)

        # Entry box for new tasks
        self.task_entry = tk.Entry(input_frame, width=30, font=("Helvetica", 12))
        self.task_entry.pack(side=tk.LEFT)

        # 'Add Task' Button
        self.add_button = tk.Button(self.root, text="Add Task", font=("Helvetica", 11, "bold"), command=self.add_task_gui)
        self.add_button.pack(pady=5)

    def add_task_gui(self):
        """GUI function to handle adding a new task."""
        # Get the task description from the entry box
        task_description = self.task_entry.get()

        if task_description:
            # For now, just show a message box.
            # Later, this will call our backend logic.
            messagebox.showinfo("Task Added", f"Task '{task_description}' added!")
            # Clear the entry box after adding the task
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "You must enter a task.")


# --- Main execution block ---
if __name__ == "__main__":
    root = tk.Tk()           # Create the main window
    app = TodoAppGUI(root)   # Create an instance of our app class
    root.mainloop()          # Start the GUI event loop