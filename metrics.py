def calculate_metrics(seek_sequence, initial_head):
    total_seek = sum(abs(seek_sequence[i] - (seek_sequence[i-1] if i > 0 else initial_head)) for i in range(len(seek_sequence)))
    avg_seek = total_seek / len(seek_sequence)
    throughput = len(seek_sequence) / 1.0  # assuming 1 time unit
    return total_seek, avg_seek, throughput
