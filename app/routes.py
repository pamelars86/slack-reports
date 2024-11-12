from flask import request, jsonify
from . import app, celery
from .tasks import fetch_messages_task
from flasgger import swag_from
from .utils import split_date_range  # Importas la función de utils.py



@app.route("/", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'API is up and running!',
            'examples': {
                'application/json': {
                    'message': 'API is up and running!'
                }
            }
        }
    }
})
def home():
    return {"message": "API is up and running!"}, 200

@app.route("/fetch-messages", methods=["POST"])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'channel': {
                        'type': 'string',
                        'example': '#general'
                    },
                    'start_date': {
                        'type': 'string',
                        'example': '2024-01-01'
                    },
                    'end_date': {
                        'type': 'string',
                        'example': '2024-01-31'
                    }
                }
            }
        }
    ],
    'responses': {
        202: {
            'description': 'Task created successfully.',
            'examples': {
                'application/json': {
                    'task_ids': [
                        'task_id_1',
                        'task_id_2',
                        'task_id_3'
                    ]
                }
            }
        }
    }
})
def fetch_messages():
    data = request.get_json()
    channel = data.get("channel")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    
    date_chunks = split_date_range(start_date, end_date)
    
    task_results = []
    for chunk in date_chunks:
        start, end = chunk
        task = fetch_messages_task.apply_async(args=[channel, start, end])
        task_results.append(task.id)
    
    return jsonify({"task_ids": task_results}), 202

@app.route("/fetch-messages-status", methods=["POST"])
def fetch_status():
    data = request.get_json()
    task_ids = data.get("task_ids")
    
    if not task_ids:
        return jsonify({"error": "No task_ids provided"}), 400

    task_statuses = []
    all_results = [] 
    all_completed = True

    for task_id in task_ids:
        task = fetch_messages_task.AsyncResult(task_id)

        if task.state == "PENDING":
            status = {"task_id": task_id, "status": "PENDING"}
            all_completed = False
        elif task.state != "FAILURE":
            status = {"task_id": task_id, "status": task.state, "result": task.result}
            if task.result:
                if isinstance(task.result, list):
                    all_results.extend(task.result)
                else:
                    all_results.append(task.result)
        else:
            status = {"task_id": task_id, "status": "FAILURE", "error": str(task.info)}

        task_statuses.append(status)

    overall_status = "COMPLETED" if all_completed else "PENDING"

    return jsonify({
        "status": overall_status, 
        "task_ids": task_statuses,
        "results": all_results
    })


@app.route("/top-repliers", methods=["POST"])
def top_repliers():
    data = request.get_json()
    channel = data.get("channel")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    return 200