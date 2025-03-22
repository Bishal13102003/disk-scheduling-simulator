from algorithms import fcfs, sstf, scan, c_scan
from visualizer import plot_schedule
from metrics import calculate_metrics

def main():
    print("Disk Scheduling Simulator")
    head = int(input("Enter initial head position: "))
    requests = list(map(int, input("Enter space-separated disk requests: ").split()))

    print("\nChoose Algorithm:")
    print("1. FCFS\n2. SSTF\n3. SCAN\n4. C-SCAN")
    choice = int(input("Enter your choice (1-4): "))

    if choice == 1:
        seek_sequence, seek_time = fcfs(requests, head)
        title = "FCFS Scheduling"
    elif choice == 2:
        seek_sequence, seek_time = sstf(requests, head)
        title = "SSTF Scheduling"
    elif choice == 3:
        direction = input("Enter direction (left/right): ").lower()
        seek_sequence, seek_time = scan(requests, head, direction)
        title = "SCAN Scheduling"
    elif choice == 4:
        seek_sequence, seek_time = c_scan(requests, head)
        title = "C-SCAN Scheduling"
    else:
        print("Invalid choice!")
        return

    print("\nSeek Sequence:", " -> ".join(map(str, seek_sequence)))
    metrics = calculate_metrics(seek_sequence, seek_time)
    print(f"Total Seek Time: {metrics['Total Seek Time']}")
    print(f"Average Seek Time: {metrics['Average Seek Time']:.2f}")

    plot_schedule(seek_sequence, title)

if __name__ == "__main__":
    main()
