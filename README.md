# Slack Reports

Application for generating reports of messages and most active users in Slack channels.

## Project Structure

```
.
├── backend/           # FastAPI Server (app)
├── frontend/          # React Application
└── README.md
```

## Frontend

### Prerequisites

- Node.js (version 14 or higher)
- npm or yarn

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

### Main Dependencies

- React 18
- TypeScript
- Tailwind CSS
- Heroicons (for icons)
- React Router (for navigation)

### Frontend Structure

```
frontend/
├── src/
│   ├── components/         # Reusable components
│   │   ├── Sidebar.tsx     # Navigation sidebar
│   │   ├── ReportForm.tsx  # Report generation form
│   │   └── TaskStatus.tsx  # Generated reports status
│   ├── types/             # TypeScript definitions
│   │   └── index.ts       # Interfaces and types
│   └── App.tsx            # Main component
├── package.json           # Dependencies and scripts
└── tsconfig.json          # TypeScript configuration
```

### Configuration

1. Ensure the backend is running at `http://localhost:5000`
2. If the backend is at a different URL, update the `API_URL` constant in `App.tsx`

### Running the Application

To start the development server:

```bash
npm start
# or
yarn start
```

The application will be available at `http://localhost:3000`

### Features

1. **Report Generation**
   - Select report type (messages or top repliers)
   - Enter channel ID
   - Specify date range
   - For top repliers, indicate how many users to show

2. **Report Tracking**
   - View status of generated reports
   - Manually update status
   - Download results in CSV or JSON format

### Main Components

1. **Sidebar**
   - Navigation between "Generate Reports" and "Report Status"
   - Responsive and user-friendly design

2. **ReportForm**
   - Intuitive form for report generation
   - Field validation
   - Report type selection with icons

3. **TaskStatus**
   - Display of each report's status
   - Update and download options
   - Detailed report information

### Styling

- Uses Tailwind CSS for styling
- Responsive design
- Light and dark themes
- Heroicons for icons

### Development

For local development:

1. Clone the repository
2. Install dependencies
3. Start the development server

## Backend

### Prerequisites

Make sure you have the following components installed:

- Python 3.8+
- Docker
- Docker Compose
- Redis (for Celery)
- Slack API Token

### Installation and Configuration

1. Clone the repository:
    ```bash
    git clone https://github.com/pamelars86/slack-reports.git
    cd slack-reports
    ```

2. Create a `.env` file in the root of the project with the following content:
    ```env
    SLACK_TOKEN=your_slack_api_token
    CELERY_BROKER_URL="redis://redis:6379/0"
    result_backend="redis://redis:6379/0"
    SLACK_HOME="https://your-organization.slack.com"
    LLAMA_HOME=""
    ```

3. Build and start the Docker containers:
    ```bash
    docker-compose up --build
    ```

5. Start the server:
    ```bash
    docker-compose up
    ```


### Usage of Endpoints

To use the endpoints for generating reports, follow these steps:

1. **Fetch Messages**: Use the `/fetch-messages` endpoint to initiate the process of fetching messages from Slack. This operation is asynchronous and will return a `task-id`.

2. **Top Repliers**: Use the `/top-repliers` endpoint to generate a report of the top repliers in your Slack workspace. This operation is also asynchronous and will return a `task-id`.

3. **Check Task Status**: To check the status of your task, use the `/task-status/{task-id}` endpoint. Replace `{task-id}` with the actual task ID you received from the previous endpoints.

For detailed information on the input and output of these endpoints, refer to the Swagger documentation available at `http://localhost:5000/apidocs/`.

### API Documentation

You can find the API documentation in Swagger by accessing the following URL once the server is up and running:

```
http://localhost:5000/apidocs/
```

### Usage

To generate reports, make sure all services are running and use the endpoints documented in Swagger.

### Contributions

Contributions are welcome. Please open an issue or a pull request to discuss any changes you would like to make.

### License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.
