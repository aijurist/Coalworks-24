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
    15: [1015, 'Amit Patel', datetime(2019, 3, 10), 28, 5, 'Environmental Engineer', 85000, 3, 'Fair', 'Night'],
    16: [1016, 'Rakesh Yadav', datetime(2018, 8, 15), 31, 2, 'Mechanic', 73000, 6, 'Good', 'Day'],
    17: [1017, 'Kiran Verma', datetime(2020, 1, 20), 29, 4, 'Mechanic', 71000, 4, 'Fair', 'Night'],
    18: [1018, 'Priya Singh', datetime(2021, 6, 10), 34, 1, 'Electrical Engineer', 77000, 7, 'Excellent', 'Day'],
    19: [1019, 'Ravi Patel', datetime(2017, 11, 30), 38, 3, 'Surveyor', 72000, 8, 'Good', 'Night'],
    20: [1020, 'Sanjay Sharma', datetime(2016, 4, 5), 45, 5, 'Hydraulic Specialist', 80000, 10, 'Good', 'Day']
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
    # No Issue/Positive Logs
    ("No issues reported", "No Issue"),
    ("Routine inspection completed successfully", "No Issue"),
    ("All operations running smoothly", "No Issue"),
    ("Team meeting held, no concerns raised", "No Issue"),
    ("Completed the task ahead of schedule", "No Issue"),

    # Delay Issues
    ("Minor delay in shovel operation due to soil conditions", "Delay"),
    ("Overburden removal delayed due to heavy rainfall", "Delay"),
    ("Material supply delayed by traffic congestion", "Delay"),
    ("Work delayed due to unforeseen circumstances", "Delay"),
    ("Operational delay in loading due to equipment issues", "Delay"),

    # Equipment Issues
    ("Drill malfunction during operation", "Equipment Issue"),
    ("Blasting equipment failed to ignite, causing delays", "Equipment Issue"),
    ("Drill performance issue affecting work speed", "Equipment Issue"),
    ("Unexpected machinery breakdown during excavation", "Equipment Issue"),
    ("Faulty conveyor belt causing material flow stoppage", "Equipment Issue"),
    ("JCB making unusual noises, needs inspection", "Equipment Issue"),
    ("Water leaking from the roof of the JCB cabin", "Equipment Issue"),
    ("Truck brake is loose, requires immediate attention", "Equipment Issue"),
    ("Flat tire on truck causing transport delays", "Equipment Issue"),

    # Maintenance Issues
    ("Routine maintenance completed", "Maintenance"),
    ("Scheduling conflict in maintenance work", "Maintenance"),
    ("Delayed maintenance work due to resource unavailability", "Maintenance"),

    # Operational Issues
    ("Power outage affecting all operations", "Operational Issue"),
    ("Supervisor is late by 12 hours", "Operational Issue"),
    ("Miscommunication between teams causing workflow issues", "Operational Issue"),
    ("System outage impacting operation tracking", "Operational Issue"),
    ("Unscheduled safety drill affecting productivity", "Operational Issue"),

    # Resource Issues
    ("Inadequate stock of essential supplies", "Resource Issue"),
    ("Shortage of critical resources affecting operations", "Resource Issue"),
    ("Insufficient fuel for machinery", "Resource Issue"),
    ("Delay in receiving materials from supplier", "Resource Issue"),
    ("Water supply issues affecting cooling systems", "Resource Issue"),

    # Human Error Issues
    ("Employee absence causing delays", "Human Error"),
    ("Mistake in task execution leading to rework", "Human Error"),
    ("Improper handling of equipment leading to damage", "Human Error"),
    ("Mislabeling of materials causing operational confusion", "Human Error"),
    ("Failure to follow safety protocol during blasting", "Human Error"),

    # Safety Issues
    ("Safety protocol breach identified", "Safety Issue"),
    ("Safety hazard identified in the workplace", "Safety Issue"),
    ("Incident involving minor injury reported", "Safety Issue"),
    ("Unsafe working conditions due to poor lighting", "Safety Issue"),
    ("Overhead structure damage posing a safety risk", "Safety Issue"),

    # Irrelevant/Unrelated Logs
    ("Discussion about weekend plans", "Irrelevant"),
    ("Weather is sunny, no issues expected", "Irrelevant"),
    ("Team discussing last night's football match", "Irrelevant"),
    ("Personal conversation about family matters", "Irrelevant"),
    ("Employee requesting a leave of absence", "Irrelevant"),
    ("Lunch break started late", "Irrelevant"),
    ("Request for additional chairs in the break room", "Irrelevant"),
    ("Talking about new office decorations", "Irrelevant"),
]

training_data_gemini = [
    # No Issue/Positive Logs
    ("No issues reported", "No Issue"),
    ("Routine inspection completed successfully", "No Issue"),
    ("All operations running smoothly", "No Issue"),
    ("Team meeting held, no concerns raised", "No Issue"),
    ("Completed the task ahead of schedule", "No Issue"),
    ("Shift change executed without issues", "No Issue"),
    ("Weekly safety drill conducted successfully", "No Issue"),
    ("Team morale is high; no problems to report", "No Issue"),
    ("All safety protocols followed during shift", "No Issue"),
    ("Production targets met without any issues", "No Issue"),

    # Delay Issues
    ("Minor delay in shovel operation due to soil conditions", "Delay"),
    ("Overburden removal delayed due to heavy rainfall", "Delay"),
    ("Material supply delayed by traffic congestion", "Delay"),
    ("Work delayed due to unforeseen circumstances", "Delay"),
    ("Operational delay in loading due to equipment issues", "Delay"),
    ("Shift start delayed due to foggy conditions", "Delay"),
    ("Waiting for replacement parts caused a delay in work", "Delay"),
    ("Delay in drilling operation due to hard rock formation", "Delay"),
    ("Power outage delayed the start of the operation", "Delay"),
    ("Loading operation delayed due to congestion at the site", "Delay"),

    # Equipment Issues
    ("Drill malfunction during operation", "Equipment Issue"),
    ("Blasting equipment failed to ignite, causing delays", "Equipment Issue"),
    ("Drill performance issue affecting work speed", "Equipment Issue"),
    ("Unexpected machinery breakdown during excavation", "Equipment Issue"),
    ("Faulty conveyor belt causing material flow stoppage", "Equipment Issue"),
    ("JCB making unusual noises, needs inspection", "Equipment Issue"),
    ("Water leaking from the roof of the JCB cabin", "Equipment Issue"),
    ("Truck brake is loose, requires immediate attention", "Equipment Issue"),
    ("Flat tire on truck causing transport delays", "Equipment Issue"),
    ("Bulldozer hydraulic system failure", "Equipment Issue"),
    ("Loader bucket malfunctioned during operation", "Equipment Issue"),
    ("Excavator arm stuck in mid-position", "Equipment Issue"),
    ("Fuel pump on generator malfunctioned", "Equipment Issue"),
    ("Conveyor belt motor overheated", "Equipment Issue"),
    ("Crane cable showing signs of wear, needs replacement", "Equipment Issue"),

    # Maintenance Issues
    ("Routine maintenance completed", "Maintenance"),
    ("Scheduling conflict in maintenance work", "Maintenance"),
    ("Delayed maintenance work due to resource unavailability", "Maintenance"),
    ("Maintenance team understaffed, causing delays", "Maintenance"),
    ("Emergency maintenance required for conveyor belt", "Maintenance"),
    ("Planned maintenance of drilling equipment postponed", "Maintenance"),
    ("Maintenance work on truck fleet started late", "Maintenance"),
    ("Maintenance team waiting for spare parts", "Maintenance"),
    ("Maintenance inspection revealed minor wear and tear", "Maintenance"),
    ("Shift maintenance completed with no major issues", "Maintenance"),

    # Operational Issues
    ("Power outage affecting all operations", "Operational Issue"),
    ("Supervisor is late by 12 hours", "Operational Issue"),
    ("Miscommunication between teams causing workflow issues", "Operational Issue"),
    ("System outage impacting operation tracking", "Operational Issue"),
    ("Unscheduled safety drill affecting productivity", "Operational Issue"),
    ("Change in shift schedule causing confusion", "Operational Issue"),
    ("Operational efficiency reduced due to lack of coordination", "Operational Issue"),
    ("Unexpected change in work orders caused delays", "Operational Issue"),
    ("Safety drill interrupted the ongoing work", "Operational Issue"),
    ("Data entry error led to incorrect production reporting", "Operational Issue"),

    # Resource Issues
    ("Inadequate stock of essential supplies", "Resource Issue"),
    ("Shortage of critical resources affecting operations", "Resource Issue"),
    ("Insufficient fuel for machinery", "Resource Issue"),
    ("Delay in receiving materials from supplier", "Resource Issue"),
    ("Water supply issues affecting cooling systems", "Resource Issue"),
    ("Low inventory of safety gear", "Resource Issue"),
    ("Fuel delivery delayed by weather conditions", "Resource Issue"),
    ("Lack of spare parts impacting maintenance schedule", "Resource Issue"),
    ("Shortage of lubricants for machinery", "Resource Issue"),
    ("Delay in arrival of explosives for blasting", "Resource Issue"),

    # Human Error Issues
    ("Employee absence causing delays", "Human Error"),
    ("Mistake in task execution leading to rework", "Human Error"),
    ("Improper handling of equipment leading to damage", "Human Error"),
    ("Mislabeling of materials causing operational confusion", "Human Error"),
    ("Failure to follow safety protocol during blasting", "Human Error"),
    ("Incorrect drill bit selection slowed progress", "Human Error"),
    ("Late arrival of workers impacted productivity", "Human Error"),
    ("Overfilling of dump truck caused spillage", "Human Error"),
    ("Incomplete documentation caused delays in task allocation", "Human Error"),
    ("Miscommunication led to improper tool usage", "Human Error"),

    # Safety Issues
    ("Safety protocol breach identified", "Safety Issue"),
    ("Safety hazard identified in the workplace", "Safety Issue"),
    ("Incident involving minor injury reported", "Safety Issue"),
    ("Unsafe working conditions due to poor lighting", "Safety Issue"),
    ("Overhead structure damage posing a safety risk", "Safety Issue"),
    ("Fire safety equipment not functional", "Safety Issue"),
    ("Blocked emergency exit found during inspection", "Safety Issue"),
    ("Hazardous materials not stored properly", "Safety Issue"),
    ("Safety inspection revealed potential risks", "Safety Issue"),
    ("Loose wiring identified as a safety hazard", "Safety Issue"),

    # Irrelevant/Unrelated Logs
    ("Discussion about weekend plans", "Irrelevant"),
    ("Weather is sunny, no issues expected", "Irrelevant"),
    ("Team discussing last night's football match", "Irrelevant"),
    ("Personal conversation about family matters", "Irrelevant"),
    ("Employee requesting a leave of absence", "Irrelevant"),
    ("Lunch break started late", "Irrelevant"),
    ("Request for additional chairs in the break room", "Irrelevant"),
    ("Talking about new office decorations", "Irrelevant"),
    ("Discussion about upcoming holidays", "Irrelevant"),
    ("Casual chat about new restaurant in town", "Irrelevant"),
    ("Team planning a social event after work", "Irrelevant"),
    ("Discussion about company-wide news", "Irrelevant"),
]



# for worker_id, data in workers_data.items():
#     print(f"{worker_id}: {data}")
    
# for worker_id, data in shift_log_data.items():
#     print(f"{worker_id}: {data[7]}")
