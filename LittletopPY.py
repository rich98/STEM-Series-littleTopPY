#rich98 (c) GNU GENERAL PUBLIC LICENSE Version 3.

import psutil
import time
import tkinter as tk

def print_top(text_widget):
    # Clear the text widget
    text_widget.delete(1.0, tk.END)

    # Get memory info
    mem_info = psutil.virtual_memory()
    text_widget.insert(tk.END, f"Total memory: {mem_info.total / (1024**3):.2f} GB\n")
    text_widget.insert(tk.END, f"Available memory: {mem_info.available / (1024**3):.2f} GB\n")
    text_widget.insert(tk.END, f"Used memory: {mem_info.used / (1024**3):.2f} GB\n")
    text_widget.insert(tk.END, f"Memory percentage used: {mem_info.percent}%\n\n")

    # Get a list of all running processes
    processes = psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info'])

    # Sort the processes by CPU usage
    processes = sorted(processes, key=lambda p: p.info['cpu_percent'], reverse=True)

    # Calculate the maximum length of the process names
    max_name_length = max(len(p.info['name']) for p in processes[:150])

    # Print the top 150 processes
    text_widget.insert(tk.END, "PID".ljust(8) + "NAME".ljust(max_name_length) + "CPU %".ljust(10) + "MEM USAGE (in MB)\n")
    for process in processes[:25]:
        mem_usage = process.info['memory_info'].rss / (1024 ** 2)  # Convert memory usage to MB
        text_widget.insert(tk.END, str(process.info['pid']).ljust(8) + process.info['name'].ljust(max_name_length) + str(process.info['cpu_percent']).ljust(10) + f"{mem_usage:.2f}\n")

def update_top(text_widget):
    print_top(text_widget)
    # Update every 5 seconds
    text_widget.after(5000, update_top, text_widget)

root = tk.Tk()
root.title("littletopPY")  # Set the window title
text_widget = tk.Text(root)
text_widget.pack()
update_top(text_widget)
root.mainloop()

