import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algorithms import fcfs, sstf, scan, c_scan

root = tk.Tk()
root.title("Disk Scheduling Simulator")
root.geometry("900x600")
root.configure(bg="#1E1E2F")
root.resizable(True, True)

colors = {
    'background': '#1E1E2F',
    'panel': '#2D2D44',
    'accent': '#4C78A8',
    'text': '#FFFFFF',
    'secondary': '#A3BFFA'
}

style = ttk.Style()
style.theme_use('clam')

style.configure("TLabel", background=colors['panel'], foreground=colors['text'], font=("Helvetica", 14))
style.configure("Title.TLabel", font=("Helvetica", 20, "bold"), foreground=colors['text'])
style.configure("Custom.TButton", background=colors['accent'], foreground=colors['text'], font=("Helvetica", 14, "bold"))
style.map("Custom.TButton", background=[('active', '#6B9AC4'), ('pressed', '#3A5F87')])
style.configure("TEntry", fieldbackground="white", foreground="black", font=("Helvetica", 12))
style.configure("TCombobox", fieldbackground="white", foreground="black", font=("Helvetica", 12))

main_frame = tk.Frame(root, bg=colors['background'])
main_frame.pack(fill="both", expand=True, padx=15, pady=15)

left_panel = tk.Frame(main_frame, bg=colors['panel'], relief="raised", bd=2)
left_panel.pack(side="left", fill="y", padx=(0, 10))

right_panel = tk.Frame(main_frame, bg=colors['panel'], relief="raised", bd=2)
right_panel.pack(side="right", fill="both", expand=True)

ttk.Label(left_panel, text="Disk Scheduling Simulator", style="Title.TLabel").pack(pady=(15, 20))

tk.Label(left_panel, text="Disk Requests (space-separated):", bg=colors['panel'], fg=colors['text'], font=("Helvetica", 14)).pack(padx=10)
entry_requests = ttk.Entry(left_panel, width=35)
entry_requests.pack(padx=10, pady=5)

tk.Label(left_panel, text="Initial Head Position:", bg=colors['panel'], fg=colors['text'], font=("Helvetica", 14)).pack(padx=10)
entry_head = ttk.Entry(left_panel, width=35)
entry_head.pack(padx=10, pady=5)

tk.Label(left_panel, text="Scheduling Algorithm:", bg=colors['panel'], fg=colors['text'], font=("Helvetica", 14)).pack(padx=10)
algo_var = tk.StringVar(value="FCFS")
algo_menu = ttk.Combobox(
    left_panel, textvariable=algo_var,
    values=["FCFS", "SSTF", "SCAN", "C-SCAN", "Adaptive"],
    state="readonly", width=32
)
algo_menu.pack(padx=10, pady=5)

recommend_text = tk.StringVar()
recommend_label = tk.Label(
    left_panel, textvariable=recommend_text,
    bg=colors['panel'], fg=colors['secondary'],
    font=("Helvetica", 12), wraplength=250
)
recommend_label.pack(padx=10, pady=5)

result_text = tk.StringVar()
result_label = tk.Label(
    right_panel, textvariable=result_text,
    font=("Consolas", 12), bg=colors['panel'],
    fg=colors['secondary'], justify="left", wraplength=400
)
result_label.pack(pady=10, padx=10)

graph_frame = tk.Frame(right_panel, bg=colors['panel'])
graph_frame.pack(fill="both", expand=True, padx=10, pady=10)

canvas = None
animation = None

def analyze_requests(requests):
    """Analyzes request pattern and recommends best algorithm"""
    if not requests:
        return "FCFS"
    
    mean = sum(requests) / len(requests)
    variance = sum((x - mean) ** 2 for x in requests) / len(requests)
    
    sorted_reqs = sorted(requests)
    avg_distance = sum(abs(sorted_reqs[i+1] - sorted_reqs[i]) 
                       for i in range(len(sorted_reqs)-1)) / (len(sorted_reqs)-1) if len(sorted_reqs) > 1 else 0
    
    if variance < 100 and avg_distance < 20:
        return "SSTF"
    elif variance > 500:
        return "SCAN"
    else:
        return "FCFS"

def run_simulation():
    """Handles input validation, runs selected algorithm, updates results and graph."""
    global canvas, animation
    try:
        requests = [int(x) for x in entry_requests.get().split()]
        head = int(entry_head.get())
        algorithm = algo_var.get()

        if algorithm == "Adaptive":
            recommended = analyze_requests(requests)
            recommend_text.set(f"Recommended: {recommended}")
            algorithm = recommended
        else:
            recommend_text.set("")

        if algorithm == "FCFS":
            sequence, total_time = fcfs(requests, head)
        elif algorithm == "SSTF":
            sequence, total_time = sstf(requests, head)
        elif algorithm == "SCAN":
            sequence, total_time = scan(requests, head)
        elif algorithm == "C-SCAN":
            sequence, total_time = c_scan(requests, head)

        avg_time = total_time / len(requests) if requests else 0
        throughput = len(sequence) / total_time if total_time > 0 else 0

        result_text.set(
            f"Algorithm: {algorithm}\n"
            f"Seek Sequence: {sequence}\n"
            f"Total Seek Time: {total_time}\n"
            f"Average Seek Time: {avg_time:.2f}\n"
            f"Throughput: {throughput:.2f} req/unit"
        )

        if canvas:
            canvas.get_tk_widget().destroy()

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.set_xlim(0, len(sequence) - 1)
        ax.set_ylim(min(sequence) - 5, max(sequence) + 5)
        ax.set_title("Disk Head Movement", color=colors['text'], fontsize=16)
        ax.set_xlabel("Step", color=colors['secondary'], fontsize=12)
        ax.set_ylabel("Cylinder Position", color=colors['secondary'], fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.3, color=colors['secondary'])
        ax.set_facecolor(colors['panel'])
        fig.set_facecolor(colors['panel'])
        ax.tick_params(colors=colors['secondary'], labelsize=10)

        line, = ax.plot([], [], '-o', color=colors['accent'], linewidth=2, markersize=8, markerfacecolor='white')

        def update(frame):
            """Updates the line for each frame in the animation."""
            line.set_data(range(frame + 1), sequence[:frame + 1])
            return line,

        animation = FuncAnimation(fig, update, frames=len(sequence), interval=500, blit=True)

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers")

ttk.Button(left_panel, text="Run Simulation", style="Custom.TButton", command=run_simulation).pack(pady=20, padx=10)

root.mainloop()