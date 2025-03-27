import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algorithms import fcfs, sstf, scan, c_scan  # Disk scheduling algorithms

# Initialize main window
root = tk.Tk()
root.title("Disk Scheduling Simulator")
root.geometry("900x600")
root.configure(bg="#1E1E2F")
root.resizable(True, True)

# Theme Colors
colors = {
    'background': '#1E1E2F',
    'panel': '#2D2D44',
    'accent': '#4C78A8',
    'text': '#FFFFFF',
    'secondary': '#A3BFFA'
}

# Configure ttk styles
style = ttk.Style()
style.theme_use('clam')

style.configure("TLabel", background=colors['panel'], foreground=colors['text'], font=("Helvetica", 11))
style.configure("Title.TLabel", font=("Helvetica", 16, "bold"), foreground=colors['text'])
style.configure("Custom.TButton", background=colors['accent'], foreground=colors['text'], font=("Helvetica", 11, "bold"))
style.map("Custom.TButton", background=[('active', '#6B9AC4'), ('pressed', '#3A5F87')])

style.configure("TEntry", fieldbackground="white", foreground="black")
style.configure("TCombobox", fieldbackground="white", foreground="black")

# Create main layout frames
main_frame = tk.Frame(root, bg=colors['background'])
main_frame.pack(fill="both", expand=True, padx=15, pady=15)

left_panel = tk.Frame(main_frame, bg=colors['panel'], relief="raised", bd=2)
left_panel.pack(side="left", fill="y", padx=(0, 10))

right_panel = tk.Frame(main_frame, bg=colors['panel'], relief="raised", bd=2)
right_panel.pack(side="right", fill="both", expand=True)

# -------------------------- LEFT PANEL (Inputs) --------------------------

# Title
ttk.Label(left_panel, text="Disk Scheduling Simulator", style="Title.TLabel").pack(pady=(15, 20))

# Disk requests input
tk.Label(left_panel, text="Disk Requests (space-separated):", bg=colors['panel'], fg=colors['text']).pack(padx=10)
entry_requests = ttk.Entry(left_panel, width=35)
entry_requests.pack(padx=10, pady=5)

# Initial head position input
tk.Label(left_panel, text="Initial Head Position:", bg=colors['panel'], fg=colors['text']).pack(padx=10)
entry_head = ttk.Entry(left_panel, width=35)
entry_head.pack(padx=10, pady=5)

# Algorithm selection dropdown
tk.Label(left_panel, text="Scheduling Algorithm:", bg=colors['panel'], fg=colors['text']).pack(padx=10)
algo_var = tk.StringVar(value="FCFS")
algo_menu = ttk.Combobox(
    left_panel, textvariable=algo_var,
    values=["FCFS", "SSTF", "SCAN", "C-SCAN"],
    state="readonly", width=32
)
algo_menu.pack(padx=10, pady=5)

# -------------------------- RIGHT PANEL (Results & Graph) --------------------------

# Label for showing results
result_text = tk.StringVar()
result_label = tk.Label(
    right_panel, textvariable=result_text,
    font=("Consolas", 10), bg=colors['panel'],
    fg=colors['secondary'], justify="left", wraplength=400
)
result_label.pack(pady=10, padx=10)

# Frame for matplotlib graph
graph_frame = tk.Frame(right_panel, bg=colors['panel'])
graph_frame.pack(fill="both", expand=True, padx=10, pady=10)

canvas = None  # Will be used for matplotlib graph embedding

# -------------------------- Simulation Logic --------------------------

def run_simulation():
    """Handles input validation, runs selected algorithm, updates results and graph."""
    global canvas
    try:
        # Get and validate inputs
        requests = [int(x) for x in entry_requests.get().split()]
        head = int(entry_head.get())
        algorithm = algo_var.get()

        # Run selected algorithm
        if algorithm == "FCFS":
            sequence, total_time = fcfs(requests, head)
        elif algorithm == "SSTF":
            sequence, total_time = sstf(requests, head)
        elif algorithm == "SCAN":
            sequence, total_time = scan(requests, head)
        elif algorithm == "C-SCAN":
            sequence, total_time = c_scan(requests, head)

        # Calculate and format metrics
        avg_time = total_time / len(requests) if requests else 0
        throughput = len(sequence) / total_time if total_time > 0 else 0

        result_text.set(
            f"Algorithm: {algorithm}\n"
            f"Seek Sequence: {sequence}\n"
            f"Total Seek Time: {total_time}\n"
            f"Average Seek Time: {avg_time:.2f}\n"
            f"Throughput: {throughput:.2f} req/unit"
        )

        # Clear previous graph if exists
        if canvas:
            canvas.get_tk_widget().destroy()

        # Plot new graph
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(
            range(len(sequence)), sequence, '-o',
            color=colors['accent'], linewidth=2,
            markersize=8, markerfacecolor='white'
        )

        ax.set_title("Disk Head Movement", color=colors['text'])
        ax.set_xlabel("Request Sequence", color=colors['secondary'])
        ax.set_ylabel("Cylinder Position", color=colors['secondary'])

        ax.grid(True, linestyle='--', alpha=0.3, color=colors['secondary'])
        ax.set_facecolor(colors['panel'])
        fig.set_facecolor(colors['panel'])
        ax.tick_params(colors=colors['secondary'])

        # Annotate points
        for i, value in enumerate(sequence):
            ax.text(i, value, str(value), ha='center', va='bottom', color=colors['text'])

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers")

# -------------------------- Action Button --------------------------
ttk.Button(left_panel, text="Run Simulation", style="Custom.TButton", command=run_simulation).pack(pady=20, padx=10)

# Start application
root.mainloop()
