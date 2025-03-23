import tkinter as tk
from tkinter import messagebox
from algorithms import fcfs, sstf, scan, c_scan
from metrics import calculate_metrics
from visualizer import plot_seek_sequence

def run_simulation():
    try:
        requests = list(map(int, entry_requests.get().split()))
        head = int(entry_head.get())
        algorithm = algo_var.get()

        if algorithm == "FCFS":
            seek_sequence, _ = fcfs(requests, head)
        elif algorithm == "SSTF":
            seek_sequence, _ = sstf(requests, head)
        elif algorithm == "SCAN":
            seek_sequence, _ = scan(requests, head)
        elif algorithm == "C-SCAN":
            seek_sequence, _ = c_scan(requests, head)
        else:
            messagebox.showerror("Error", "Invalid algorithm selected!")
            return

        total_seek, avg_seek, throughput = calculate_metrics(seek_sequence, head)
        result = (
            f"Seek Sequence: {seek_sequence}\n"
            f"Total Seek Time: {total_seek}\n"
            f"Average Seek Time: {avg_seek:.2f}\n"
            f"Throughput: {throughput:.2f} requests/unit time"
        )
        output_label.config(text=result)

        plot_seek_sequence(seek_sequence, head)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")


root = tk.Tk()
root.title("Disk Scheduling Simulator")
root.geometry("500x450")

tk.Label(root, text="Enter disk requests (space-separated):").pack()
entry_requests = tk.Entry(root, width=50)
entry_requests.pack(pady=5)

tk.Label(root, text="Enter initial head position:").pack()
entry_head = tk.Entry(root, width=30)
entry_head.pack(pady=5)

tk.Label(root, text="Select Scheduling Algorithm:").pack()
algo_var = tk.StringVar(value="FCFS")
tk.OptionMenu(root, algo_var, "FCFS", "SSTF", "SCAN", "C-SCAN").pack(pady=5)

tk.Button(root, text="Run Simulation", command=run_simulation).pack(pady=10)

output_label = tk.Label(root, text="", justify="left", font=("Courier", 10))
output_label.pack(pady=10)

root.mainloop()

