def load_process_file(filepath):
    """
    Parses the input file to retrieve process data.
    Expected format: #pid arrival_time burst_time priority
    """
    processes = []
    
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            
            # Ignore empty lines and comments
            if not line or line.startswith("#"):
                continue
            
            # Split the line by spaces or tabs
            parts = line.split()
            
            # Check if the line has exactly 4 columns
            if len(parts) != 4:
                continue
                
            pid, arrival, burst, priority = parts
            
            processes.append({
                "pid": pid,
                "arrival": int(arrival),
                "burst": int(burst),
                "priority": int(priority),
                "remaining_time": int(burst),
                "start_time": -1,
                "finish_time": 0
            })
            
    # Sort the processes based on arrival time
    processes.sort(key=lambda x: x['arrival'])
    return processes