from flask import request, jsonify
from . import app, celery
from .tasks import fetch_messages_task, calculate_top_repliers_task, summarize_thread_task
from flasgger import swag_from
from .utils import validate_date_format, validate_dates, validate_top_n, get_channel_id


TASK_MAPPING = {
    'fetch_messages': fetch_messages_task,
    'top_repliers': calculate_top_repliers_task,
    'summarize_thread': summarize_thread_task
}

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
    try:
        data = request.get_json()
        channel_id = data.get("channel_id")
        start_date_str = data.get("start_date")
        end_date_str = data.get("end_date")

        start_date = validate_date_format(start_date_str)
        end_date = validate_date_format(end_date_str)
        
        if not start_date or not end_date:
             jsonify({"error": "Dates must be in the format YYYY-MM-DD"}), 400

        error_message = validate_dates(start_date, end_date)
        if error_message:
            return jsonify({"error": error_message}), 400

        task = fetch_messages_task.apply_async(args=[channel_id, start_date_str, end_date_str])

        return jsonify({"task_id": task.id}), 202

    except Exception as e:
            return jsonify({"error": str(e)}), 400


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

    try:
        data = request.get_json()
        channel_id = data.get("channel_id")
        start_date_str = data.get("start_date")
        end_date_str = data.get("end_date")
        top_n = data.get('top_n')
        
        start_date = validate_date_format(start_date_str)
        end_date = validate_date_format(end_date_str)
        if not start_date or not end_date:
             jsonify({"error": "Dates must be in the format YYYY-MM-DD"}), 400

        error_message = validate_dates(start_date, end_date)
        if error_message:
            return jsonify({"error": error_message}), 400

        top_n = validate_top_n(top_n)
        
        # Lanza la tarea de Celery en segundo plano
        task = calculate_top_repliers_task.delay(channel_id, start_date_str, end_date_str, top_n)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    
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
        },
        {
            'name': 'task_name',
            'in': 'query',
            'required': False,
            'type': 'string',
            'description': 'The name of the task using _'
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
    task_name = request.args.get('task_name')
    
    if task_name and task_name in TASK_MAPPING:
        task = TASK_MAPPING[task_name].AsyncResult(task_id)
    else:
        return jsonify({"status": "FAILURE", "error": "Invalid task_name"}), 400

    if task.state == 'PENDING':
        return jsonify({"status": "PENDING"}), 202
    elif task.state == 'SUCCESS':
        return jsonify({"status": "SUCCESS", "data": task.result}), 200
    elif task.state == 'FAILURE':
        return jsonify({"status": "FAILURE", "error": str(task.info)}), 500
    else:
        return jsonify({"status": task.state}), 202

@app.route("/summarize-thread", methods=["POST"])
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
                        'example': 'C1234567890',
                        'description': 'The Slack channel ID'
                    },
                    'thread_ts': {
                        'type': 'string',
                        'example': '1748458889.115369',
                        'description': 'The thread timestamp'
                    },
                    'llm_provider': {
                        'type': 'string',
                        'example': 'openai',
                        'description': 'LLM provider to use (openai or ollama)',
                        'enum': ['openai', 'ollama']
                    }
                },
                'required': ['channel_id', 'thread_ts', 'llm_provider']
            }
        }
    ],
    'responses': {
        202: {
            'description': 'Thread summarization task created successfully.',
            'examples': {
                'application/json': {
                    'task_id': 'task_id_1'
                }
            }
        },
        400: {
            'description': 'Bad request - missing or invalid parameters.',
            'examples': {
                'application/json': {
                    'error': 'Missing required parameter: channel_id'
                }
            }
        }
    }
})
def summarize_thread():
    """Endpoint to summarize a Slack thread using LLM"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        channel_id = data.get("channel_id")
        thread_ts = data.get("thread_ts")
        llm_provider = data.get("llm_provider")
        model = data.get("model")
        
        # Validate required parameters
        if not channel_id:
            return jsonify({"error": "Missing required parameter: channel_id"}), 400
        if not thread_ts:
            return jsonify({"error": "Missing required parameter: thread_ts"}), 400
        if not llm_provider:
            return jsonify({"error": "Missing required parameter: llm_provider"}), 400
        if not model:
            return jsonify({"error": "Missing required parameter: model"}), 400
        
        # Validate LLM provider
        if llm_provider.lower() not in ['openai', 'ollama']:
            return jsonify({"error": "Invalid llm_provider. Must be 'openai' or 'ollama'"}), 400
        
        # Launch Celery task
        task = summarize_thread_task.apply_async(args=[channel_id, thread_ts, llm_provider.lower(), model])
        
        return jsonify({"task_id": task.id}), 202
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400
