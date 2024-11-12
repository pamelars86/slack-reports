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
