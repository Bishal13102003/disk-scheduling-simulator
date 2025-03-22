import matplotlib.pyplot as plt

def plot_schedule(seek_sequence, title="Disk Scheduling Algorithm"):
    plt.figure(figsize=(8, 4))
    plt.plot(seek_sequence, range(len(seek_sequence)), marker='o', linestyle='-', color='b')
    plt.xlabel("Cylinder Number")
    plt.ylabel("Sequence of Execution")
    plt.title(title)
    plt.grid()
    plt.show()
