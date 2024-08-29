import pandas as pd
from datetime import datetime

workers_data = {
    1: [1001, 'Rajesh Kumar', datetime(2015, 6, 1), 45, 1, 'Excavator Operator', 75000, 10, 'Good', 'Day'],
    2: [1002, 'Anita Sharma', datetime(2017, 9, 15), 38, 2, 'Geologist', 85000, 7, 'Excellent', 'Night'],
    3: [1003, 'Vikram Singh', datetime(2018, 2, 20), 29, 3, 'Shovel Operator', 68000, 5, 'Fair', 'Day'],
    4: [1004, 'Sita Devi', datetime(2020, 11, 10), 42, 1, 'Mine Safety Inspector', 90000, 12, 'Good', 'Night'],
    5: [1005, 'Arjun Patel', datetime(2021, 5, 5), 35, 4, 'Drilling Specialist', 72000, 8, 'Excellent', 'Day'],
    6: [1006, 'Meena Reddy', datetime(2014, 7, 22), 50, 2, 'Blasting Technician', 78000, 15, 'Good', 'Day'],
    7: [1007, 'Ravi Kumar', datetime(2019, 1, 30), 33, 3, 'Maintenance Engineer', 83000, 6, 'Fair', 'Night'],
    8: [1008, 'Lakshmi Rao', datetime(2016, 8, 10), 40, 1, 'Loader Operator', 71000, 9, 'Good', 'Day'],
    9: [1009, 'Ajay Patel', datetime(2022, 3, 12), 28, 4, 'Surveyor', 69000, 3, 'Excellent', 'Night'],
    10: [1010, 'Nisha Agarwal', datetime(2019, 11, 25), 31, 5, 'Environmental Engineer', 84000, 6, 'Good', 'Day'],
    11: [1011, 'Gopal Reddy', datetime(2018, 4, 10), 36, 3, 'Shovel Operator', 67000, 7, 'Fair', 'Night'],
    12: [1012, 'Sunita Devi', datetime(2016, 12, 5), 39, 1, 'Loader Operator', 70000, 8, 'Good', 'Night'],
    13: [1013, 'Raj Kumar', datetime(2022, 7, 15), 32, 4, 'Drilling Specialist', 71000, 4, 'Good', 'Night'],
    14: [1014, 'Geeta Sharma', datetime(2021, 10, 20), 30, 2, 'Blasting Technician', 79000, 5, 'Excellent', 'Day'],
    15: [1015, 'Amit Patel', datetime(2019, 3, 10), 28, 5, 'Environmental Engineer', 85000, 3, 'Fair', 'Night']
}

shift_log_data = {
   # 0: ['Worker ID', 'Name', 'Date', 'Shift Start', 'Shift End', 'Hours Worked', 'Task', 'Remarks'],
    1: [1001, 'Rajesh Kumar', datetime(2024, 8, 1), datetime(2024, 8, 1, 8, 0), datetime(2024, 8, 1, 16, 0), 8, 'Excavation', 'No issues'],
    2: [1003, 'Vikram Singh', datetime(2024, 8, 1), datetime(2024, 8, 1, 8, 0), datetime(2024, 8, 1, 16, 0), 8, 'Shovel Operation', 'Minor delay in shovel operation'],
    3: [1005, 'Arjun Patel', datetime(2024, 8, 2), datetime(2024, 8, 2, 8, 0), datetime(2024, 8, 2, 16, 0), 8, 'Drilling', 'Drill malfunction'],
    4: [1006, 'Meena Reddy', datetime(2024, 8, 2), datetime(2024, 8, 2, 8, 0), datetime(2024, 8, 2, 16, 0), 8, 'Blasting', 'Blasting equipment issue; Delay in OBD removal'],
    5: [1008, 'Lakshmi Rao', datetime(2024, 8, 3), datetime(2024, 8, 3, 8, 0), datetime(2024, 8, 3, 16, 0), 8, 'Loader Operation', 'No issues'],
    6: [1010, 'Nisha Agarwal', datetime(2024, 8, 3), datetime(2024, 8, 3, 8, 0), datetime(2024, 8, 3, 16, 0), 8, 'Environmental Check', 'All tasks completed']
}

training_data = [
    # No Issue
    ("No issues", "No Issue"),
    ("The work was completed", "No Issue"),
    ("Routine inspection completed without issues", "No Issue"),

    # Delay
    ("Minor delay in shovel operation", "Delay"),
    ("Overburden removal delay due to weather", "Delay"),
    ("Delay in material supply", "Delay"),
    ("Work delayed due to unforeseen circumstances", "Delay"),

    # Equipment Issue
    ("Drill malfunction", "Equipment Issue"),
    ("Blasting equipment issue; Delay in OBD removal", "Equipment Issue"),
    ("Drill performance issue", "Equipment Issue"),
    ("Unexpected machinery breakdown", "Equipment Issue"),
    ("Faulty conveyor belt", "Equipment Issue"),

    # Maintenance
    ("Routine maintenance", "Maintenance"),
    ("Maintenance scheduling conflict", "Maintenance"),

    # Operational Issue
    ("Power outage affecting operations", "Operational Issue"),
    ("Overtime work due to shift handover delays", "Operational Issue"),
    ("Unexpected increase in workload", "Operational Issue"),
    ("Supervisor is late by 12 hours", "Operational Issue"),

    # Resource Issue
    ("Insufficient raw material", "Resource Issue"),
    ("Delayed delivery of spare parts", "Resource Issue"),
    ("Inadequate stock of essential supplies", "Resource Issue"),
    ("Shortage of critical resources", "Resource Issue"),

    # Human Error
    ("Operator error causing delays", "Human Error"),
    ("Incorrectly set machine parameters", "Human Error"),
    ("Employee absence causing delays", "Human Error"),
    ("Mistake in task execution", "Human Error"),

    # Safety Issue
    ("Safety protocol breach", "Safety Issue"),
    ("Emergency evacuation drill conducted", "Safety Issue"),
    ("Safety gear not available", "Safety Issue"),
    ("Safety hazard identified in workplace", "Safety Issue"),
]


# for worker_id, data in workers_data.items():
#     print(f"{worker_id}: {data}")
    
# for worker_id, data in shift_log_data.items():
#     print(f"{worker_id}: {data[7]}")
