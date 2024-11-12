from flask import request, jsonify
from . import app, celery
from .tasks import fetch_messages_task
from flasgger import swag_from
from .tasks import calculate_top_repliers_task



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
                    'channel_id': {
                        'type': 'string',
                        'example': 'ABC123'
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
                    'task_id': 'task_id_1'
                }
            }
        },
    }
})
def fetch_messages():
    data = request.get_json()
    channel_id = data.get("channel_id")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    task = fetch_messages_task.apply_async(args=[channel_id, start_date, end_date])

    return jsonify({"task_id": task.id}), 202


@app.route("/top-repliers", methods=["POST"])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'channel_id': {
                        'type': 'string',
                        'example': 'ABC123'
                    },
                    'start_date': {
                        'type': 'string',
                        'example': '2024-01-01'
                    },
                    'end_date': {
                        'type': 'string',
                        'example': '2024-01-31'
                    },
                    'top': {
                        'type': 'integer',
                        'example': 5
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
                    'task_id': 'task_id_1'
                }
            }
        },
    }
})
def top_repliers():
    data = request.get_json()
    channel_id = data.get("channel_id")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    top_n = data.get('top')
    
    # Lanza la tarea de Celery en segundo plano
    task = calculate_top_repliers_task.delay(channel_id, start_date, end_date, top_n)
    
    return jsonify({"task_id": task.id}), 202


@app.route('/task-status/<task_id>', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'task_id',
            'in': 'path',
            'required': True,
            'type': 'string',
            'description': 'The ID of the task'
        }
    ],
    'responses': {
        202: {
            'description': 'Task is still pending or in progress.',
            'examples': {
                'application/json': {
                    'status': 'PENDING'
                }
            }
        },
        200: {
            'description': 'Task completed successfully.',
            'examples': {
                'application/json': {
                    'status': 'SUCCESS',
                    'data': {}
                }
            }
        },
        500: {
            'description': 'Task failed.',
            'examples': {
                'application/json': {
                    'status': 'FAILURE',
                    'error': 'Error message'
                }
            }
        }
    }
})
def get_task_status(task_id):
    task = calculate_top_repliers_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        return jsonify({"status": "PENDING"}), 202
    elif task.state == 'SUCCESS':
        return jsonify({"status": "SUCCESS", "data": task.result}), 200
    elif task.state == 'FAILURE':
        return jsonify({"status": "FAILURE", "error": str(task.info)}), 500
    else:
        return jsonify({"status": task.state}), 202
    
