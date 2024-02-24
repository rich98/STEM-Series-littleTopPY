# littleTopPY

`littletopPY` is a simple Python script that mimics some of the functionality of the Linux `top` command. It uses the `psutil` and `tkinter` libraries to gather system and process information and display it in a GUI window.

### Requirements
This script requires the psutil library to gather system and process information. You can install it using pip:

pip install psutil

### Usage
You can run this script from the command line like any other Python script:

python littletopPY.py

This will open a new window that displays the total, available, and used memory, as well as the percentage of memory used, and the PID, name, CPU usage, and memory usage of the top 150 processes, updating every 5 seconds.
## Code Explanation

The script consists of three main functions: `print_top`, `update_top`, and `clear_screen`.

### print_top Function

```python
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

    # Print the top 150 processes
    text_widget.insert(tk.END, "PID".ljust(8) + "NAME".ljust(25) + "CPU %".ljust(10) + "MEM USAGE (in MB)\n")
    for process in processes[:150]:
        mem_usage = process.info['memory_info'].rss / (1024 ** 2)  # Convert memory usage to MB
        text_widget.insert(tk.END, str(process.info['pid']).ljust(8) + process.info['name'].ljust(25) + str(process.info['cpu_percent']).ljust(10) + f"{mem_usage:.2f}\n")
