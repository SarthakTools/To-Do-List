import customtkinter as ctk
import json
from datetime import datetime
from PIL import Image
import os
from customtkinter import *

image_path = os.path.join(os.path.dirname(os.path.relpath(__file__)), "images")
trash_image = CTkImage(Image.open(os.path.join(image_path, "trash.png")), size=(25, 25))


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced To-Do List")
        self.root.geometry("500x600")
        self.root.iconbitmap("images\\to_do_list.ico")
        
        # Set the appearance mode to "Dark" without the option to change
        ctk.set_appearance_mode("dark")
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#1E1E2E")  # Dark background
        self.main_frame.pack(fill="both", expand=True)
        
        self.tasks = []
        self.load_tasks()
        
        self.selected_tasks = set()  # New set to keep track of selected tasks
        self.checkboxes = []  # List to store checkbox references
        
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = ctk.CTkLabel(self.main_frame, text="Enhanced To-Do List 📝", font=("Helvetica", 24, "bold"), text_color="white")
        title_label.pack(pady=(20, 15))
        

        # Task input frame
        input_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=20)
        
        # Task input
        self.task_input = ctk.CTkEntry(input_frame, placeholder_text="Enter a task", 
                                       fg_color="#2A2A3C", text_color="white", 
                                       placeholder_text_color="#6C6C7C",
                                       height=40, corner_radius=20, font=("monospace", 20, "normal"))
        self.task_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.task_input.bind("<Return>", lambda event: self.add_task())  # Add this line
        
        # Add button
        add_button = ctk.CTkButton(input_frame, text="Add Task", fg_color="#FF6B6B", 
                                   hover_color="#FF8787", text_color="white", 
                                   width=80, height=40, corner_radius=20,
                                   command=self.add_task, font=("Poppins", 15))
        add_button.pack(side="right")

        # Task list frame
        task_list_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        task_list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Task list (scrollable frame)
        self.task_list = ctk.CTkScrollableFrame(task_list_frame, fg_color="#2A2A3C", corner_radius=10)
        self.task_list.pack(fill="both", expand=True)

        # Statistics
        self.stats_label = ctk.CTkLabel(self.main_frame, text="", text_color="white")
        self.stats_label.pack(pady=5)

        # Add buttons for multi-delete functionality
        multi_delete_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        multi_delete_frame.pack(pady=10)

        select_all_button = ctk.CTkButton(multi_delete_frame, text="Select All", command=self.select_all_tasks,
                                          fg_color="#3A3A4C", hover_color="#4A4A5C")
        select_all_button.pack(side="left", padx=5)

        deselect_all_button = ctk.CTkButton(multi_delete_frame, text="Deselect All", command=self.deselect_all_tasks,
                                              fg_color="#3A3A4C", hover_color="#4A4A5C")
        deselect_all_button.pack(side="left", padx=5)

        delete_selected_button = ctk.CTkButton(multi_delete_frame, text="Delete Selected", 
                                               command=self.delete_selected_tasks,
                                                fg_color="#FF6B6B", hover_color="#FF8787", text_color="white")
        delete_selected_button.pack(side="left", padx=5)

        self.update_task_list()

    def add_task(self):
        task = self.task_input.get()
        if task:
            self.tasks.append({
                "text": task,
                "completed": False,
                "created_at": datetime.now().isoformat()
            })
            self.task_input.delete(0, ctk.END)
            self.update_task_list()
            self.save_tasks()

    def update_task_list(self):
        for widget in self.task_list.winfo_children():
            widget.destroy()
        
        self.checkboxes.clear()

        for i, task in enumerate(self.tasks):
            task_frame = ctk.CTkFrame(self.task_list, fg_color="transparent")
            task_frame.pack(fill="x", pady=5)

            checkbox = ctk.CTkCheckBox(task_frame, text=task["text"], 
                                       command=lambda i=i: self.toggle_task_completion(i),
                                       fg_color="#FF6B6B", hover_color="#FF8787", text_color="white", font=("Poppins", 18))
            checkbox.pack(side="left", padx=5)
            if task["completed"]:
                checkbox.select()
            else:
                checkbox.deselect()
            self.checkboxes.append(checkbox)

            delete_button = ctk.CTkButton(task_frame, text="", width=30, fg_color="transparent", 
                                          text_color="#FF6B6B", hover_color="#444",
                                          command=lambda i=i: self.delete_task(i), image=trash_image)
            delete_button.pack(side="right", padx=10)

            created_at = datetime.fromisoformat(task["created_at"]).strftime("%Y-%m-%d %H:%M")
            date_label = ctk.CTkLabel(task_frame, text=created_at, font=("Helvetica", 15), text_color="#a5a5a5")
            date_label.pack(side="right", padx=10)

        self.update_statistics()

    def update_statistics(self):
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for task in self.tasks if task["completed"])
        stats_text = f"Total tasks: {total_tasks} | Completed: {completed_tasks} | Remaining: {total_tasks - completed_tasks}"
        self.stats_label.configure(text=stats_text)

    def toggle_task_completion(self, i):
        self.tasks[i]["completed"] = not self.tasks[i]["completed"]
        self.update_statistics()
        self.save_tasks()

    def delete_task(self, i):
        del self.tasks[i]
        self.update_task_list()
        self.save_tasks()

    def delete_selected_tasks(self):
        self.tasks = [task for task in self.tasks if not task["completed"]]
        self.update_task_list()
        self.save_tasks()

    def select_all_tasks(self):
        for i, task in enumerate(self.tasks):
            task["completed"] = True
            self.checkboxes[i].select()
        self.update_statistics()
        self.save_tasks()

    def deselect_all_tasks(self):
        for i, task in enumerate(self.tasks):
            task["completed"] = False
            self.checkboxes[i].deselect()
        self.update_statistics()
        self.save_tasks()

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
        except FileNotFoundError:
            pass

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = ctk.CTk()
    app = TodoApp(root)
    app.run()