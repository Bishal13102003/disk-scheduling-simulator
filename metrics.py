def calculate_metrics(seek_sequence, seek_time):
    avg_seek_time = seek_time / (len(seek_sequence) - 1)
    return {"Total Seek Time": seek_time, "Average Seek Time": avg_seek_time}
