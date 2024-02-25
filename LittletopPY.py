import psutil
import time
import tkinter as tk
import platform

def print_top(text_widget):
    # Clear the text widget before updating
    text_widget.delete('1.0', tk.END)

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
    text_widget.insert(tk.END, "This script may report Windows 11 as Windows 10. This is not a bug.\n")
    text_widget.insert(tk.END, "answers.microsoft.com – Win11 Shows Win10 as OS\n")
    
    os_info = platform.uname()
    text_widget.insert(tk.END, f"Operating System: {os_info.system}, OS Release: {os_info.release}, OS Version: {os_info.version}\n\n") 

    # Get the top 25 processes
    processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']), key=lambda p: p.info['cpu_percent'], reverse=True)

    # Calculate the maximum length of the process names
    max_name_length = max(len(p.info['name']) for p in processes[:25])

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

