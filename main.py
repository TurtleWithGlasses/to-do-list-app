import tkinter as tk
from tkinter import ttk, messagebox
import json

class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = int(screen_width * 0.6)
        window_height = int(screen_height * 0.8)
        self.root.geometry(f"{window_width}x{window_height}")

        # Frames
        self.left_frame = tk.Frame(root, width=(window_width * 0.75), height=window_height)
        self.left_frame.pack_propagate(False)  # Prevent frame from resizing with its content
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Treeview with fixed size
        style = ttk.Style()
        # increase row height to make checkboxes bigger
        style.configure("Treeview", rowheight=30) 

        self.tree = ttk.Treeview(self.left_frame, columns=("Task", "Status"), show="headings", height=46)
        self.tree.heading("Task", text="Task")
        self.tree.heading("Status", text="Finished")
        self.tree.column("Task", width=int(window_width * 0.55))  # Fixed width for Task column
        self.tree.column("Status", width=120, anchor=tk.CENTER)  # Fixed width for Status column
        self.tree.pack(expand=False, fill=tk.NONE)  # Prevent resizing

        # Entry in the right frame
        self.entry = tk.Entry(self.right_frame, width=30)
        self.entry.pack(pady=5)

        #  add & remove buttons side by side
        self.button_frame1 = tk.Frame(self.right_frame)
        self.button_frame1.pack(pady=5)

        self.add_button = tk.Button(self.button_frame1, text="Add", command=self.add_item, width=12)
        self.add_button.pack(side=tk.LEFT)

        self.remove_button = tk.Button(self.button_frame1, text="Remove", command=self.remove_item, width=12)
        self.remove_button.pack(side=tk.RIGHT)

        # Up & Down buttons side by side
        self.button_frame2 = tk.Frame(self.right_frame)
        self.button_frame2.pack(pady=5)
        
        self.up_button = tk.Button(self.button_frame2, text="Up", command=lambda: self.move_item(-1), width=12)
        self.up_button.pack(side=tk.LEFT)

        self.down_button = tk.Button(self.button_frame2, text="Down", command=lambda: self.move_item(1), width=12)
        self.down_button.pack(side=tk.RIGHT)

        # reset and edit buttons

        self.button_frame3 = tk.Frame(self.right_frame)
        self.button_frame3.pack(pady=5)
        
        self.reset_button = tk.Button(self.button_frame3, text="Reset", command=self.reset_list, width=12)
        self.reset_button.pack(side=tk.RIGHT)

        self.edit_button = tk.Button(self.button_frame3, text="Edit", command=self.edit_item, width=12)
        self.edit_button.pack(side=tk.LEFT)

        # Load the list from file
        self.load_list()

    def add_item(self):
        item_text = self.entry.get()
        if item_text:
            self.tree.insert("", tk.END, values=(item_text, "☐"))
            self.entry.delete(0, tk.END)
            self.save_list()
        else:
            messagebox.showwarning("Warning", "You must enter a task.")

    def remove_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
            self.save_list()
        else:
            messagebox.showwarning("Warning", "You must select a task to remove.")

    def move_item(self, direction):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item)
            new_index = index + direction
            if 0 <= new_index < len(self.tree.get_children()):
                item_values = self.tree.item(selected_item, 'values')
                self.tree.delete(selected_item)
                self.tree.insert("", new_index, values=item_values)
                self.tree.selection_set(self.tree.get_children()[new_index])
                self.save_list()
        else:
            messagebox.showwarning("Warning", "You must select a task to move.")

    def reset_list(self):
        for item in self.tree.get_children():
            self.tree.item(item, values=(self.tree.item(item, 'values')[0], "☐"))
        self.save_list()

    def toggle_status(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            current_status = self.tree.item(item, 'values')[1]
            new_status = "☑" if current_status == "☐" else "☐"
            self.tree.item(item, values=(self.tree.item(item, 'values')[0], new_status))
            self.save_list()

    def edit_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            current_text = self.tree.item(selected_item, "values")[0]
            new_text = self.entry.get()
            if new_text:
                self.tree.item(selected_item, values=(new_text, "☐"))  # Corrected method call
                self.entry.delete(0, tk.END)
                self.save_list()
            else:
                messagebox.showwarning("Warning", "You must enter a new task.")
        else:
            messagebox.showwarning("Warning", "You must select a task to edit.")

    def save_list(self):
        tasks = [(self.tree.item(item, 'values')[0], self.tree.item(item, 'values')[1]) for item in self.tree.get_children()]
        with open("todo_list.json", "w") as f:
            json.dump(tasks, f)

    def load_list(self):
        try:
            with open("todo_list.json", "r") as f:
                tasks = json.load(f)
                for task, status in tasks:
                    self.tree.insert("", tk.END, values=(task, status))
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoListApp(root)
    app.tree.bind("<Double-1>", app.toggle_status)  # Bind double-click to toggle checkbox
    root.mainloop()