# Slack Reports

This project allows generating reports from data obtained from Slack.

## Prerequisites

Make sure you have the following components installed:

- Python 3.8+
- Docker
- Docker Compose
- Redis (for Celery)
- Slack API Token

## Installation and Configuration

1. Clone the repository:
    ```bash
    git clone https://github.com/pamelars86/slack-reports.git
    cd slack-reports
    ```

2. Create a `.env` file in the root of the project with the following content:
    ```env
    SLACK_API_TOKEN=your_slack_api_token
    CELERY_BROKER_URL=""
    result_backend=""
    ```

3. Build and start the Docker containers:
    ```bash
    docker-compose up --build
    ```

5. Start the server:
    ```bash
    docker-compose up
    ```

## Running Tests

To run the tests, follow these steps:

1. Make sure you have installed the development dependencies:

    ```bash
    poetry install --with dev
    ```

2. Run the tests using `pytest`:

    ```bash
    poetry run pytest
    ```

This will execute all the tests in the `tests` directory and provide a report of the test results.


## Usage of Endpoints

To use the endpoints for generating reports, follow these steps:

1. **Fetch Messages**: Use the `/fetch-messages` endpoint to initiate the process of fetching messages from Slack. This operation is asynchronous and will return a `task-id`.

2. **Top Repliers**: Use the `/top-repliers` endpoint to generate a report of the top repliers in your Slack workspace. This operation is also asynchronous and will return a `task-id`.

3. **Check Task Status**: To check the status of your task, use the `/task-status/{task-id}` endpoint. Replace `{task-id}` with the actual task ID you received from the previous endpoints.

For detailed information on the input and output of these endpoints, refer to the Swagger documentation available at `http://localhost:5000/apidocs/`.


## API Documentation

You can find the API documentation in Swagger by accessing the following URL once the server is up and running:

```
http://localhost:5000/apidocs/
```

## Usage

To generate reports, make sure all services are running and use the endpoints documented in Swagger.

## Contributions

Contributions are welcome. Please open an issue or a pull request to discuss any changes you would like to make.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
