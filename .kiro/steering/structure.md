# Project Structure

## Repository Organization

The repository follows a multi-agent architecture with each agent as a self-contained module:

```
ads_agents_demo/
├── README.md                           # Main project documentation
├── GETTING_STARTED.md                  # Quick start guide
├── ads_creative_agent/                 # Creative generation agent
├── ads_buget_allocation_agent/         # Budget optimization agent  
├── ads_data_analyst_agent/             # Data analysis agent
├── ads-materials-understand-agent/     # Material understanding agent
└── pre-advertising-analysis-agent/     # Pre-advertising analysis agent
```

## Individual Agent Structure

Each agent follows a consistent structure pattern:

```
agent_name/
├── README.md                   # Agent-specific documentation
├── requirements.txt            # Python dependencies
├── agent.py                    # Core agent logic with Strands framework
├── run_ui.py                   # Standard Streamlit UI launcher
├── run_nlp_ui.py              # NLP-enabled UI launcher (when available)
├── run_demo_ui.py             # Demo UI launcher (when available)
├── ui.py                      # Streamlit UI implementation
├── demo_app.py                # Demo application (when available)
├── api_server.py              # REST API server (when available)
├── tests/                     # Test files
├── temp/                      # Temporary files and processing
├── output/                    # Generated outputs
├── repl_state/                # Agent state persistence
├── bak/                       # Backup files and old versions
└── [agent-specific modules]   # Custom modules per agent
```

## Common File Patterns

### Core Agent Files
- `agent.py` - Main agent implementation using Strands framework
- `*_agent.py` - Alternative agent implementations
- `simple_agent.py` - Simplified agent versions

### UI Files
- `ui.py` - Main Streamlit interface
- `demo_ui.py` - Demo-specific UI
- `run_*.py` - UI launcher scripts with different configurations

### API Files
- `api_server.py` - FastAPI REST server
- `api_client.py` - API client utilities
- `test_api.py` - API testing scripts

### Utility Files
- `image_handler.py` - Image processing utilities
- `resize_images.py` - Image resizing functionality
- `utils.py` - General utilities
- `custom_callback_handler.py` - Strands callback customization

### Configuration Files
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Multi-service orchestration
- `nginx.conf` - Reverse proxy configuration

## Naming Conventions

### Directories
- Use lowercase with underscores: `ads_creative_agent`
- Hyphens for compound names: `ads-materials-understand-agent`

### Python Files
- Snake case: `budget_allocation_agent.py`
- Descriptive prefixes: `run_`, `test_`, `demo_`

### UI Launchers
- `run_ui.py` - Standard interface
- `run_nlp_ui.py` - Natural language interface
- `run_demo_ui.py` - Demo interface

## Data Organization

### Input Data
- CSV files in agent root: `google.campaign_daily_geo_stats.csv`
- Test data in `test_data/` subdirectory
- Sample files with descriptive names

### Output Data
- `output/` - Generated files and results
- `temp/` - Temporary processing files
- `downloaded_images/` - Downloaded assets
- `repl_state/` - Agent state persistence

## Development Patterns

### Agent Implementation
- Use Strands framework as base: `from strands import Agent, tool`
- Import tools from `strands_tools`
- Implement custom tools with `@tool` decorator
- Use BedrockModel for LLM integration

### UI Implementation
- Streamlit as primary framework
- Custom CSS for consistent styling
- Wide layout configuration
- Sidebar for controls and settings

### Error Handling
- Structured logging with strands integration
- Error directories for debugging: `errors/`
- Graceful fallbacks in UI components