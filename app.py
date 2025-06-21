import tkinter as tk
from tkinter import ttk

# Initialize main window
root = tk.Tk()
root.title("TO-DO APP")
root.geometry("400x550")
root.resizable(False, False)
root.configure(bg="#c5d8a2")

# Background pattern canvas
canvas = tk.Canvas(root, width=400, height=550, bg="#c5d8a2", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Outer frame
frame_outer = tk.Frame(canvas, bg="#c5d8a2", bd=15, relief="ridge")
frame_outer.place(relx=0.5, rely=0.5, anchor="center", width=360, height=500)

# Title
label = tk.Label(frame_outer, text="Enter Your Task", font=("calibri", 14, "bold"), bg="#c5d8a2")
label.pack(pady=10)

# Task Entry 
task_entry = tk.Entry(frame_outer, width=30)
task_entry.pack(pady=5)

# Task storage and progress bar
tasks = []
progress = ttk.Progressbar(frame_outer, orient="horizontal", length=320, mode="determinate")
progress.pack(pady=(10, 0))
progress_label = tk.Label(frame_outer, text="0% Complete", bg="#c5d8a2", font=("calibri", 9))
progress_label.pack()

# Functions
def update_progress():
    total = len(tasks)
    completed = sum(1 for task in tasks if task.startswith("[✔]"))
    percent = int((completed / total) * 100) if total > 0 else 0
    progress["value"] = percent
    progress_label.config(text=f"{percent}% Complete")

def refresh_listbox():
    listbox.delete(0, tk.END)
    for i, task in enumerate(tasks, start=1):
        listbox.insert(tk.END, f"{i}. {task}")
        bg_color = '#63e370' if task.startswith("[✔]") else 'white'
        listbox.itemconfig(i - 1, {'bg': bg_color})
    update_progress()

def add_task():
    task_text = task_entry.get().strip()
    if task_text:
        tasks.append(task_text)
        task_entry.delete(0, tk.END)
        refresh_listbox()

def delete_task():
    try:
        index = listbox.curselection()[0]
        tasks.pop(index)
        refresh_listbox()
    except IndexError:
        pass

def toggle_task_complete(event):
    try:
        index = listbox.curselection()[0]
        task = tasks[index]
        if task.startswith("[✔] "):
            tasks[index] = task.replace("[✔] ", "")
        else:
            tasks[index] = "[✔] " + task
        refresh_listbox()
    except IndexError:
        pass

def save_tasks():
    with open("tasks.txt", "w") as file:
        for i, task in enumerate(tasks, start=1):
            file.write(f"{i}. {task}\n")

def load_tasks():
    try:
        with open("tasks.txt", "r") as file:
            for line in file:
                if ". " in line:
                    task_text = line.strip().split(". ", 1)[1]
                    tasks.append(task_text)
        refresh_listbox()
    except FileNotFoundError:
        pass

def clear_all_tasks():
    tasks.clear()
    refresh_listbox()

def add_and_save_task(event=None):
    add_task()
    save_tasks()
    
# Hover effects
def on_enter(e):
    e.widget['background'] = '#86a591'  # Hover color
def on_leave(e):
    e.widget['background'] = "#86a591" # Restore original color
    
# List and scrollbar
list_frame = tk.Frame(frame_outer, bg="#c5d8a2")
list_frame.pack(expand=True, fill='both', padx=10)
style = ttk.Style()
style.theme_use("default")

# Configure the vertical scrollbar style
style.configure("Vertical.TScrollbar",
    gripcount=0,
    background="#a3c9a8",     # Scrollbar thumb color
    darkcolor="#709775",      # Shadow
    lightcolor="#d4eac7",     # Highlight
    troughcolor="#e1f0da",    # Background of the scrollbar track
    bordercolor="#b4c8a1",    # Border around the scrollbar
    arrowcolor="#2c3e50",     # Arrow (up/down) color
    relief="flat",
    width=12
)
scrollbar = ttk.Scrollbar(list_frame, orient="vertical", style="Vertical.TScrollbar", command=...)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Active state (hover or click)
style.map("Vertical.TScrollbar",
    background=[('active', '#88b394')],
    arrowcolor=[('active', '#1e2a38')]
)

listbox = tk.Listbox(list_frame, width=34, height=10, bg='#c5d8a2' ,yscrollcommand=scrollbar.set, activestyle='none')
listbox.pack(side=tk.LEFT, fill='both', expand=True)
listbox.bind("<Double-Button-1>", toggle_task_complete)

scrollbar.config(command=listbox.yview)
task_entry.bind("<Return>", add_and_save_task)

# Buttons
btn_frame = tk.Frame(frame_outer, bg="white")
btn_frame.pack(pady=10)

delete_btn=tk.Button(btn_frame, text="Delete Task", width=14, command=delete_task)
delete_btn.grid(row=0, column=0, padx=5)
delete_btn.bind("<Enter>", on_enter)
delete_btn.bind("<Leave>", on_leave)

clear_btn=tk.Button(btn_frame, text="Clear All", width=14, command=clear_all_tasks)
clear_btn.grid(row=1, column=0, padx=5, pady=5)
clear_btn.bind("<Enter>", on_enter)
clear_btn.bind("<Leave>", on_leave)

# Load data at start
load_tasks()
# Run the app
root.mainloop()
