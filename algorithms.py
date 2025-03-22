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
    left, right = [], []

    for req in requests:
        if req < head:
            left.append(req)
        else:
            right.append(req)

    if direction == "right":
        seek_sequence = [head] + right + left[::-1]
    else:
        seek_sequence = [head] + left[::-1] + right

    seek_time = sum(abs(seek_sequence[i] - seek_sequence[i-1]) for i in range(1, len(seek_sequence)))
    return seek_sequence, seek_time

def c_scan(requests, head, disk_size=200):
    requests.sort()
    left, right = [], []

    for req in requests:
        if req < head:
            left.append(req)
        else:
            right.append(req)

    seek_sequence = [head] + right + [disk_size, 0] + left
    seek_time = sum(abs(seek_sequence[i] - seek_sequence[i-1]) for i in range(1, len(seek_sequence)))
    return seek_sequence, seek_time
