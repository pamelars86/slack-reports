# Slack Reports

Application for generating reports of messages and most active users in Slack channels, with AI-powered thread summarization.

## Project Structure

```
.
├── backend/           # FastAPI Server (app)
├── frontend/          # React Application
└── README.md
```

## Cómo Ejecutar la Aplicación

### Levantar el Frontend

1. **Navegar al directorio del frontend:**
   ```bash
   cd frontend
   ```

2. **Instalar dependencias:**
   ```bash
   npm install
   # o
   yarn install
   ```

3. **Iniciar el servidor de desarrollo:**
   ```bash
   npm start
   # o
   yarn start
   ```

4. **Acceder a la aplicación:**
   - La aplicación estará disponible en `http://localhost:3000`
   - Asegúrate de que el backend esté ejecutándose en `http://localhost:5000`

### Levantar el Backend

1. **Configurar variables de entorno** (ver sección Backend para detalles)

2. **Ejecutar con Docker:**
   ```bash
   docker-compose up --build
   ```

3. **El backend estará disponible en `http://localhost:5000`**

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

2. **Thread Summarization** (NEW)
   - Generate AI-powered summaries of Slack threads
   - Support for OpenAI and Ollama LLM providers
   - Input thread timestamp and channel ID

3. **Report Tracking**
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
- OpenAI API Key (optional, for OpenAI summarization)
- Ollama (optional, for local LLM summarization)

### Installation and Configuration

1. Clone the repository:
    ```bash
    git clone https://github.com/pamelars86/slack-reports.git
    cd slack-reports
    ```

2. Create a `.env` file in the root of the project with the following content:
    ```env
    # Slack Configuration
    SLACK_TOKEN=your_slack_api_token
    SLACK_HOME="https://your-organization.slack.com"
    
    # Redis Configuration
    CELERY_BROKER_URL="redis://redis:6379/0"
    result_backend="redis://redis:6379/0"
    
    # OpenAI Configuration (optional)
    OPENAI_API_KEY=your_openai_api_key
    OPENAI_MODEL=gpt-3.5-turbo
    
    # Ollama Configuration (optional)
    OLLAMA_HOST=http://localhost:11434
    OLLAMA_MODEL=llama3
    ```

3. Build and start the Docker containers:
    ```bash
    docker-compose up --build
    ```

4. Start the server:
    ```bash
    docker-compose up
    ```

### New AI Summarization Features

#### Thread Summarization
The application now supports AI-powered summarization of Slack threads using either OpenAI or Ollama:

- **OpenAI Integration**: Uses GPT models for high-quality summaries
- **Ollama Integration**: Uses local LLM models for privacy-focused summarization
- **Configurable Prompts**: Prompts are stored in `app/prompts.yml` for easy customization
- **Flexible Architecture**: Abstract interface allows easy addition of new LLM providers

#### LLM Architecture
- `LLMInterface`: Abstract base class for all LLM implementations
- `OpenAILLM`: OpenAI API implementation
- `OllamaLLM`: Ollama local model implementation  
- `LLMFactory`: Factory pattern for creating appropriate LLM instances
- Prompts stored in YAML for easy modification without code changes

### Usage of Endpoints

To use the endpoints for generating reports, follow these steps:

1. **Fetch Messages**: Use the `/fetch-messages` endpoint to initiate the process of fetching messages from Slack. This operation is asynchronous and will return a `task-id`.

2. **Top Repliers**: Use the `/top-repliers` endpoint to generate a report of the top repliers in your Slack workspace. This operation is also asynchronous and will return a `task-id`.

3. **Thread Summarization** (NEW): Use the `/summarize-thread` endpoint to generate AI summaries of Slack threads:
   ```json
   {
     "channel_id": "C1234567890",
     "thread_ts": "1748458889.115369",
     "llm_provider": "openai"
   }
   ```

4. **Check Task Status**: To check the status of your task, use the `/task-status/{task-id}` endpoint. Replace `{task-id}` with the actual task ID you received from the previous endpoints.

For detailed information on the input and output of these endpoints, refer to the Swagger documentation available at `http://localhost:5000/apidocs/`.

### API Documentation

You can find the API documentation in Swagger by accessing the following URL once the server is running:

```
http://localhost:5000/apidocs/
```

### Usage

To generate reports and summaries, make sure all services are running and use the endpoints documented in Swagger.

### Contributions

Contributions are welcome. Please open an issue or a pull request to discuss any changes you would like to make.

### License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.
