def fcfs(requests, head):
    seek_sequence = [head] + requests
    seek_time = sum(abs(seek_sequence[i] - seek_sequence[i-1]) for i in range(1, len(seek_sequence)))
    return seek_sequence, seek_time

def sstf(requests, head):
    remaining = requests[:]
    seek_sequence = [head]
    seek_time = 0

    while remaining:
        closest = min(remaining, key=lambda x: abs(x - head))
        seek_time += abs(closest - head)
        head = closest
        seek_sequence.append(head)
        remaining.remove(closest)

    return seek_sequence, seek_time

def scan(requests, head, direction="right", disk_size=200):
    requests.sort()
    left = [req for req in requests if req < head]
    right = [req for req in requests if req >= head]

    seek_sequence = [head]

    if direction == "right":
        seek_sequence += right
        if left:
            seek_sequence += [disk_size - 1]
            seek_sequence += left[::-1]
    else:
        seek_sequence += left[::-1]
        if right:
            seek_sequence += [0]
            seek_sequence += right

    seek_time = sum(abs(seek_sequence[i] - seek_sequence[i-1]) for i in range(1, len(seek_sequence)))
    return seek_sequence, seek_time

def c_scan(requests, head, disk_size=200):
    requests.sort()
    left = [req for req in requests if req < head]
    right = [req for req in requests if req >= head]

    seek_sequence = [head] + right

    if left:
        seek_sequence += [disk_size - 1, 0] + left

    seek_time = sum(abs(seek_sequence[i] - seek_sequence[i-1]) for i in range(1, len(seek_sequence)))
    return seek_sequence, seek_time
