# Technology Stack

## Core Framework

- **Strands Framework**: Primary AI agent framework for building intelligent agents
  - `strands-agents`: Core agent functionality
  - `strands-agents-tools`: Pre-built tools (file_read, file_write, http_request, python_repl, etc.)
  - `strands.models.BedrockModel`: AWS Bedrock integration for LLM access

## AI/ML Services

- **AWS Bedrock**: Primary LLM provider
  - Amazon Nova models (nova-lite-v1:0, nova-pro-v1:0)
  - Anthropic Claude models (claude-3-7-sonnet)
  - Amazon Nova Canvas for image generation
- **Exa API**: Web search and research capabilities

## Web Framework

- **Streamlit**: Primary UI framework for all agent interfaces
  - Standard ports: 8501 (main), 8503 (creative agent)
  - Custom CSS styling for consistent branding
  - File upload and download capabilities

## Data Processing

- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Plotly**: Interactive data visualization
- **OpenCV**: Image processing and computer vision

## Infrastructure

- **Docker**: Containerization with multi-service support
- **Docker Compose**: Service orchestration
- **Nginx**: Reverse proxy and load balancing
- **FastAPI + Uvicorn**: REST API services (port 8000)

## Common Commands

### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run individual agents
python run_ui.py          # Standard UI
python run_nlp_ui.py      # NLP-enabled UI
python run_demo_ui.py     # Demo interface
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build

# Individual container
docker build -t agent-name .
docker run -p 8501:8501 -p 8000:8000 agent-name
```

### Testing
```bash
# Run tests (when available)
python -m pytest tests/

# API testing
python test_api.py
```

## Environment Configuration

- **AWS Configuration**: Required for Bedrock access
- **Environment Variables**: 
  - `DEV=true` for development mode
  - `AWS_DEFAULT_REGION=us-east-1`
- **Logging**: Structured logging with strands framework integration