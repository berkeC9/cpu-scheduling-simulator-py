def run_priority_p(processes):
    """
    Preemptive Priority Scheduling.
    Lower integer value indicates higher scheduling priority.
    """
    active_procs = [p.copy() for p in processes]
    n = len(processes)

    current_time = 0
    completed_count = 0
    gantt = []
    log = []
    context_switches = 0
    last_proc = None

    while completed_count < n:
        # Check arrivals
        for p in active_procs:
            if p['arrival'] == current_time:
                log.append(f"t={current_time}: {p['pid']} arrives [Prio:{p['priority']}]")

        ready = [p for p in active_procs if p['arrival'] <= current_time and p['remaining_time'] > 0]

        if not ready:
            current_time += 1
            continue

        # Preemptive selection: Priority -> Arrival -> PID
        ready.sort(key=lambda x: (x['priority'], x['arrival'], x['pid']))
        current_proc = ready[0]

        # Context Switch / Preemption Logic
        if last_proc != current_proc:
            if last_proc is not None and last_proc['remaining_time'] > 0:
                log.append(f"t={current_time}: {current_proc['pid']} preempts {last_proc['pid']}")
                context_switches += 1
            elif last_proc is not None:
                context_switches += 1

            if current_proc['start_time'] == -1:
                current_proc['start_time'] = current_time
                log.append(f"t={current_time}: {current_proc['pid']} starts running")
            else:
                log.append(f"t={current_time}: {current_proc['pid']} resumes")

        last_proc = current_proc

        current_proc['remaining_time'] -= 1

        # Timeline update
        if gantt and gantt[-1]['pid'] == current_proc['pid'] and gantt[-1]['end'] == current_time:
            gantt[-1]['end'] += 1
        else:
            gantt.append({"pid": current_proc['pid'], "start": current_time, "end": current_time + 1})

        current_time += 1

        if current_proc['remaining_time'] == 0:
            current_proc['finish_time'] = current_time
            completed_count += 1
            log.append(f"t={current_time}: {current_proc['pid']} completes")

    return {
        "gantt": gantt,
        "history_log": log,
        "completed_processes": [p for p in active_procs if p['remaining_time'] == 0],
        "context_switches": context_switches
    }
