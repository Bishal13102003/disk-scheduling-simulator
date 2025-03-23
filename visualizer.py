import matplotlib.pyplot as plt

def plot_seek_sequence(seek_sequence, head):
    positions = [head] + seek_sequence
    plt.figure(figsize=(8, 5))
    plt.plot(range(len(positions)), positions, marker='o', linestyle='-')
    plt.title("Disk Head Movement")
    plt.xlabel("Sequence")
    plt.ylabel("Cylinder")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
