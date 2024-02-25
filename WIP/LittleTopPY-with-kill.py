import psutil
import time
import tkinter as tk
import platform
from tkinter import *
from tkinter import simpledialog

# Global flag to control whether to refresh data or not
refresh_data = True

def print_top(root, text_widget):
    # Get CPU stats for each core
    cpu_percentages = psutil.cpu_percent(percpu=True)
    for i in range(0, len(cpu_percentages), 3):
        cpu_stats = ', '.join([f"CPU Core {j}: {cpu_percentages[j]}%" for j in range(i, min(i + 3, len(cpu_percentages)))])
        text_widget.insert(tk.END, cpu_stats + '\n')

    # Add an empty line
    text_widget.insert(tk.END, '\n')

    # Get network stats
    net_info = psutil.net_io_counters()
    net_stats = f"Network Info - Bytes Sent: {net_info.bytes_sent / (1024**3):.2f} GB, Bytes Received: {net_info.bytes_recv / (1024**3):.2f} GB\n\n"
    text_widget.insert(tk.END, net_stats)
    
    # Get memory info
    mem_info = psutil.virtual_memory()
    memory_stats = f"Memory Info - Total: {mem_info.total / (1024**3):.2f} GB, Available: {mem_info.available / (1024**3):.2f} GB, Used: {mem_info.used / (1024**3):.2f} GB, Usage Percentage: {mem_info.percent}%\n\n"
    text_widget.insert(tk.END, memory_stats)

    # Get operating system info
    text_widget.insert(tk.END, "this scrpt may report Windows 11 as Windows 10. This is not a bug\n")
    text_widget.insert(tk.END, "answers.microsoft.com – Win11 Shows Win10 as OS\n")
    
    os_info = platform.uname()
    text_widget.insert(tk.END, f"Operating System: {os_info.system}, OS Release: {os_info.release}, OS Version: {os_info.version}\n\n") 
    
    
    # Get a list of all running processes
    
    processes = psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info'])

    # Sort the processes by CPU usage
    processes = sorted(processes, key=lambda p: p.info['cpu_percent'], reverse=True)

    # Calculate the maximum length of the process names
    max_name_length = max(len(p.info['name']) for p in processes[:150])

    # Print the top 25 processes
    text_widget.insert(tk.END, "PID".ljust(8) + "NAME".ljust(max_name_length) + "CPU %".ljust(10) + "MEM USAGE (in MB)\n")
    for process in processes[:150]:
        mem_usage = process.info['memory_info'].rss / (1024 ** 2)  # Convert memory usage to MB
        line = str(process.info['pid']).ljust(8) + process.info['name'].ljust(max_name_length) + str(process.info['cpu_percent']).ljust(10) + f"{mem_usage:.2f}\n"
        text_widget.insert(tk.END, line)

def update_top(root):
    global refresh_data
    # Clear all widgets from the root window
    for widget in root.winfo_children():
        widget.destroy()

    # Recreate the text widget
    text_widget = tk.Text(root)
    text_widget.pack(expand=True, fill='both')  # Make the text widget expand to fill the window

    if refresh_data:
        print_top(root, text_widget)
        # Update every 5 seconds
        root.after(5000, update_top, root)

def kill_process_by_pid(root):
    global refresh_data
    # Pause data refreshing
    refresh_data = False
    pid = simpledialog.askinteger("Kill Process", "Enter PID of process to kill")
    if pid is not None:
        try:
            process = psutil.Process(pid)
            process.terminate()
        except psutil.NoSuchProcess:
            print(f"No process found with PID {pid}")
        except Exception as e:
            print(f"An error occurred: {e}")
    # Resume data refreshing
    refresh_data = True
    update_top(root)

root = tk.Tk()
root.title("littletopPY")  # Set the window title
root.resizable(True, True)  # Make the window resizable

# Bind Alt-K to kill_process_by_pid function
root.bind('<Alt-k>', lambda event: kill_process_by_pid(root))

text_widget = tk.Text(root)
text_widget.pack(expand=True, fill='both')  # Make the text widget expand to fill the window

update_top(root)
root.mainloop()
