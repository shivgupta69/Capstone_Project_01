def generate_schedule(tasks):
    """Build a simple study timeline by descending task duration."""
    schedule = []
    current_time = 9

    tasks = sorted(tasks, key=lambda x: x[4], reverse=True)

    for task in tasks:
        schedule.append(
            {
                "task": task[2],
                "category": task[3],
                "start": current_time,
                "end": current_time + task[4],
            }
        )
        current_time += task[4]

    return schedule
