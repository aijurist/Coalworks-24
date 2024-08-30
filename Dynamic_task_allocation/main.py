from datetime import datetime, timedelta
from dummy_data import workers_data

def assign_task_next_shift(issue_classification, workers_data, current_time):
    task_assignment = {}
    
    # Define shift start times
    day_shift_start = current_time.replace(hour=6, minute=0, second=0, microsecond=0)  # 6 AM
    night_shift_start = current_time.replace(hour=18, minute=0, second=0, microsecond=0)  # 6 PM
    if current_time >= day_shift_start and current_time < night_shift_start:
        next_shift_start = night_shift_start
        next_shift = "Night"
    else:
        # Current shift is Night, next shift is Day
        next_shift_start = day_shift_start + timedelta(days=1)  # Next day
        next_shift = "Day"
    
    # Define task categories and roles
    task_mapping = {
        "Equipment Issue": ["Maintenance Engineer", "Mechanic"],
        "Delay": ["Supervisor", "Geologist"],
        "Safety Issue": ["Mine Safety Inspector", "Environmental Engineer"],
        "Operational Issue": ["Excavator Operator", "Loader Operator"],
        "Resource Issue": ["Surveyor", "Blasting Technician"],
        "Human Error": ["Supervisor", "Training Officer"],
        "No Issue": []
    }
    
    for worker_id, details in workers_data.items():
        if details[5] in task_mapping[issue_classification]:
            if details[9] == next_shift:
                if task_assignment.get(issue_classification, None) is None or details[7] < task_assignment[issue_classification][7]:
                    task_assignment[issue_classification] = details

    # Handle edge cases
    if issue_classification in task_assignment:
        return task_assignment[issue_classification]
    else:
        return "No worker available in the next shift. Flagging for manual review."

# Example usage
current_time = datetime.now()  # Current datetime
issue_classification = 'Equipment Issue'

assigned_worker = assign_task_next_shift(issue_classification, workers_data, current_time)
print(f"Assigned Worker for Next Shift: {assigned_worker}")
