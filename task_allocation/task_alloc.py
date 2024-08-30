from flask import Blueprint, request, jsonify
from gemini_task import classification_model, training_data_gemini
from worker import workers_data
import requests

# Create a Blueprint instance
task_allocation = Blueprint('task_allocation', __name__)

classification_url = 'http://127.0.0.1:5000/tasks/remark'

def get_issue_classification(log_detail):
    res = requests.post(classification_url, json=log_detail)
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception(f"Failed to get classification: {res.status_code}")


def supervisor_notification(issue_type, location=None, is_warning=False):
    if is_warning:
        return f"Warning supervisor about {issue_type}"
    else:
        return f"Notifying supervisor about {issue_type} at location {location}"


def get_worker_by_id(worker_id):
    return next((w for w in workers_data if w['User_id'] == worker_id), None)


def get_next_shift(current_shift):
    shifts = ["Shift 1", "Shift 2", "Shift 3"]
    shift_index = shifts.index(current_shift)
    next_shift_index = (shift_index + 1) % len(shifts)
    return shifts[next_shift_index]


def find_workers_role_shift(role_id, shift):
    return [w for w in workers_data if w['Role_id'] == role_id and w['Shift'] == shift]


def find_mechanics_in_next_shift(current_shift):
    next_shift = get_next_shift(current_shift)
    return [w for w in workers_data if w['Role_id'] in ['507', '602'] and w['Shift'] == next_shift]


def assign_task(log_detail, worker_id):
    worker = get_worker_by_id(worker_id)
    if not worker:
        return {"status": "Worker not found"}

    role_id = worker.get('Role_id', None)  # Get role_id from the worker data
    if not role_id:
        return {"status": "Role ID not found for the worker"}

    issue_classification = get_issue_classification(log_detail)
    issue_type = issue_classification.get('classification', 'Unknown')
    
    current_shift = worker.get('Shift', '')

    if issue_type == 'Equipment Issue':
        mechanic = find_mechanics_in_next_shift(current_shift)
        next_shift_role_workers = find_workers_role_shift(role_id, get_next_shift(current_shift))
        
        if mechanic and next_shift_role_workers:
            mechanic = mechanic[0]
            assigned_worker = next_shift_role_workers[0]
            return {
                "status": "Task assigned",
                "mechanic": mechanic,
                "worker": assigned_worker,
                "location": log_detail.get('location', 'Unknown')
            }
        else:
            return {"status": "No available worker or mechanic in next shift"}

    elif issue_type in ['Delay', 'Resource Issue', 'Human Error Issues']:
        # Notify supervisor
        supervisor_msg = supervisor_notification(issue_type, log_detail.get('location', 'Unknown'))
        next_shift_workers = find_workers_role_shift(role_id, get_next_shift(current_shift))
        
        if next_shift_workers:
            worker = next_shift_workers[0]
            return {
                "status": "Task assigned",
                "worker": worker,
                "supervisor_msg": supervisor_msg
            }
        else:
            return {"status": "No available worker with the same role in next shift", "supervisor_msg": supervisor_msg}

    elif issue_type == 'Safety Issue':
        # Contact supervisor with warning
        supervisor_msg = supervisor_notification(issue_type, is_warning=True)
        next_shift_workers = find_workers_role_shift(role_id, get_next_shift(current_shift))
        if next_shift_workers:
            worker = next_shift_workers[0]
            return {"status": "Injury reported", "supervisor_msg": supervisor_msg, "worker": worker}
        else:
            return {"status": "No available worker with the same role in next shift", "supervisor_msg": supervisor_msg}

    elif issue_type == 'No Issue':
        next_shift_workers = find_workers_role_shift(role_id, get_next_shift(current_shift))
        return {"worker": next_shift_workers[0], "message": "Task allocated"}
    
    else:
        return {"status": "Unknown issue type"}


@task_allocation.route('/remark', methods=['POST'])
def remark():
    try:
        data = request.json
        log_data = data.get('log_data', {})
        if not log_data:
            return jsonify({"error": "No log_data provided"}), 400

        # Call the classification model
        res = classification_model.invoke({
            "training_data": training_data_gemini,
            "log_data": log_data
        })
        
        return jsonify(res)

    except Exception as e:
        # Handle exceptions
        return jsonify({"error": str(e)}), 500


@task_allocation.route('/assign_task', methods=['POST'])
def assign_task_route():
    data = request.json
    log_detail = data.get('log_detail', {})
    worker_id = data.get('worker_id')

    result = assign_task(log_detail, worker_id)
    return jsonify(result)
