import tkinter as tk
from tkinter import ttk
import time
import json
import os

class TaskTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Tracker")
        self.root.configure(bg='#a9def9')
        self.active_task = None
        self.start_time = None
        self.task_durations = self.load_task_durations()
        self.timer_running = False

        self.create_ui()

    def create_ui(self):
        self.container_colors = ['#00afb9', '#003049', '#3a5a40', '#ef233c']
        self.containers = ['Container 1', 'Container 2', 'Container 3', 'Container 4']

        for i, container in enumerate(self.containers):
            frame = tk.Frame(self.root, bg=self.container_colors[i])
            frame.grid(row=i // 2, column=i % 2, sticky="nsew", padx=10, pady=10)
            button = tk.Button(frame, text=container, bg='#eb5e28', fg='white', borderwidth=2, relief="solid", command=lambda c=container: self.start_task(c))
            button.pack(expand=True, fill="both")
            self.root.grid_columnconfigure(i % 2, weight=1)
            self.root.grid_rowconfigure(i // 2, weight=1)

        self.timer_frame = tk.Frame(self.root, bg='#a9def9')
        self.timer_label = tk.Label(self.timer_frame, text="Timer: 0.00 seconds", bg='#a9def9')
        self.timer_label.pack(pady=10)

        self.stop_button = tk.Button(self.timer_frame, text="Stop", bg='#eb5e28', fg='white', borderwidth=2, relief="solid", command=self.stop_task)
        self.stop_button.pack(pady=5)

        self.notes_frame = tk.Frame(self.root, bg='#a9def9')
        self.notes_label = tk.Label(self.notes_frame, text="Notes:", bg='#a9def9')
        self.notes_label.pack(pady=5)

        self.notes_text = tk.Text(self.notes_frame, height=4, width=50)
        self.notes_text.pack(pady=5)

        self.submit_button = tk.Button(self.notes_frame, text="Submit", bg='#eb5e28', fg='white', borderwidth=2, relief="solid", command=self.submit_task)
        self.submit_button.pack(pady=5)

    def start_task(self, container):
        self.active_task = container
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()
        self.show_timer_frame()

    def show_timer_frame(self):
        self.clear_window()
        self.timer_frame.pack(expand=True, fill="both", padx=20, pady=20)

    def stop_task(self):
        if self.timer_running:
            end_time = time.time()
            self.duration = end_time - self.start_time
            self.timer_running = False
            self.timer_label.config(text=f"Timer: {self.duration:.2f} seconds")
            self.show_notes_frame()

    def show_notes_frame(self):
        self.clear_window()
        self.timer_frame.pack(expand=True, fill="both", padx=20, pady=20)
        self.notes_frame.pack(expand=True, fill="both", padx=20, pady=20)

    def submit_task(self):
        notes = self.notes_text.get("1.0", tk.END).strip()
        self.save_task_duration(self.active_task, self.duration, notes)
        self.notes_text.delete("1.0", tk.END)
        self.return_to_initial_screen()

    def return_to_initial_screen(self):
        self.clear_window()
        self.create_ui()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()
            widget.grid_forget()

    def update_timer(self):
        if self.timer_running:
            elapsed_time = time.time() - self.start_time
            self.timer_label.config(text=f"Timer: {elapsed_time:.2f} seconds")
            self.root.after(100, self.update_timer)

    def save_task_duration(self, task, duration, notes):
        task_data = {
            'duration': duration,
            'notes': notes
        }
        if task in self.task_durations:
            self.task_durations[task].append(task_data)
        else:
            self.task_durations[task] = [task_data]
        self.save_task_durations()

    def load_task_durations(self):
        if os.path.exists('task_durations.json'):
            with open('task_durations.json', 'r') as file:
                return json.load(file)
        return {}

    def save_task_durations(self):
        with open('task_durations.json', 'w') as file:
            json.dump(self.task_durations, file)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskTracker(root)
    root.mainloop()