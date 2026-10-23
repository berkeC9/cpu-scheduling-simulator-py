def display_gantt_chart(timeline):
    """
    Renders a text-based Gantt chart 
    | P1 | P2 | P3 |
    0    5    10   15
    """
    if not timeline:
        print("No execution timeline available.")
        return

    # Top row for processes, Bottom row for time markers
    top_row = "|"
    bottom_row = str(timeline[0]['start'])

    # Track the length of the bottom row
    last_index = len(bottom_row)

    for entry in timeline:
        pid = entry['pid']
        start = entry['start']
        end = entry['end']
        
        # Cell content 
        cell_content = f" {pid} "
        
        # Check for IDLE state 
        if start > int(bottom_row.strip().split()[-1]):
             idle_content = " IDLE "
             top_row += idle_content + "|"
             
             # Add spaces to the bottom row to match the IDLE gap
             spaces_needed = len(top_row) - len(bottom_row) - len(str(start))
             bottom_row += " " * spaces_needed + str(start)

        # Add the normal process block
        top_row += cell_content + "|"

        # Align the time marker in the bottom row
        target_len = len(top_row) - len(str(end))
        
        # Calculate how much padding is needed
        current_len = len(bottom_row)
        padding = target_len - current_len
        
        if padding > 0:
            bottom_row += " " * padding + str(end)
        else:
            # If the number doesn't fit , add a single space
            bottom_row += " " + str(end)

    print(top_row)
    print(bottom_row)