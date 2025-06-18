# Browser Automation API

This FastAPI service wraps the browser automation functionality using CDP (Chrome DevTools Protocol).

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure Chrome/Chromium is running with remote debugging enabled:
```bash
google-chrome --remote-debugging-port=9222
```

3. Set up your AWS credentials for Bedrock access in your environment variables or .env file.

## Running the API

Start the FastAPI server:
```bash
uvicorn browser_api:app --reload
```

The API will be available at http://localhost:8000

## API Endpoints

### POST /execute_task

Execute a browser automation task.

Request body:
```json
{
    "task": "Your task description",
    "cdp_url": "http://localhost:9222",  // Optional, defaults to this value
    "max_steps": 30  // Optional, defaults to 30
}
```

Example task:
```json
{
    "task": "Visit cnn.com, navigate to the 'World News' section, and identify the latest headline"
}
```

### GET /health

Health check endpoint that returns the API status.

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc