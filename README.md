# ADS Agents Demo

This repository contains a comprehensive demonstration of AI-powered advertising analysis agents that can process, analyze, and classify advertising data across multiple formats.

## Project Overview

The ADS Agents Demo is a suite of AI-powered tools designed to help marketers and advertising professionals make data-driven decisions. The project consists of three main modules:

1. **Pre-Advertising Analysis Agent**: Focuses on website analysis and advertising strategy development
2. **Ads Materials Understanding Agent**: Specializes in analyzing and categorizing video content
3. **Integrated UI**: Combines all agents into a unified interface

Together, these modules provide a complete toolkit for understanding and optimizing advertising content across different media formats.

## Project Structure

```
ads_agents_demo/
├── install.py                         # Installation script
├── requirements.txt                   # Root-level dependencies
├── streamlit_ui.py                    # Main Streamlit UI entry point
├── temp/                              # Shared temporary files
│
├── pre-advertising-analysis-agent/    # Website analysis module
│   ├── ads_analysis_ui.py            # UI for ads analysis
│   ├── browser_use_ui.py             # UI for browser automation
│   ├── browser_use/                  # Browser automation components
│   │   ├── agent/                    # AI agent for browser control
│   │   ├── browser/                  # Browser interaction components
│   │   ├── controller/               # Browser control logic
│   │   ├── dom/                      # DOM manipulation utilities
│   │   └── telemetry/                # Browser telemetry collection
│   ├── mcp-server/                   # Model Control Protocol server
│   │   └── fastmcp-test/             # MCP testing components
│   ├── multi-agents/                 # Multi-agent coordination
│   └── requirements.txt              # Dependencies for this module
│
└── ads-materials-understand-agent/    # Video analysis module
    ├── agent.py                      # Core agent implementation
    ├── app.py                        # Streamlit application
    ├── requirements.txt              # Dependencies for this module
    ├── temp/                         # Temporary video files
    ├── test_data/                    # Sample videos for testing
    └── tools_test/                   # Utility scripts for testing
```

## Key Features

### Pre-Advertising Analysis Agent

- **Website Deep Analysis**
  - Product analysis: Understand product positioning, features, and pricing strategies
  - Competitor analysis: Identify main competitors and compare differences
  - Market analysis: Analyze market size, trends, and opportunities
  - Audience analysis: Study target audience characteristics and behaviors
  - SEO insights: Evaluate website optimization and keyword effectiveness

- **Browser Automation**
  - AI-driven: Uses Amazon Bedrock Claude model to control the browser
  - Real-time visualization: View browser operations through VNC/CDP
  - Flexible configuration: Adjust execution steps and connection parameters
  - Automatic reporting: Generate structured analysis reports
  - Remote CDP support: Connect to remote browser instances
  - Screenshot capture: Visual documentation of website elements

- **Multi-Agent Coordination**
  - Agent graph architecture for complex tasks
  - Coordinated analysis across multiple domains
  - Shared memory and context between agents

### Ads Materials Understanding Agent

- **Video Content Understanding**
  - Upload local video files (supports mp4, mov, avi formats)
  - Download and analyze videos via URL
  - Understand video content using Amazon Nova Pro
  - Automatically classify videos into 278 predefined categories
  - Display detailed classification results
  - User-friendly interface with video preview
  - Frame-by-frame analysis capabilities

- **Multiple Analysis Methods**
  - File upload: Analyze locally stored videos
  - URL analysis: Process videos from web sources
  - Chat-based analysis: Interact with the agent through conversation
  - Batch processing: Handle multiple videos sequentially
  - Comparative analysis: Compare multiple videos for similarities and differences

### Integrated UI

- **Unified Interface**
  - Single entry point for all analysis tools
  - Consistent design and user experience
  - Seamless switching between different analysis modes
  - Integrated results display
  - Form-based inputs for easy configuration
  - Real-time feedback on analysis progress

## Technology Stack

- **AI Models**
  - Amazon Bedrock (Claude 3.7 Sonnet) - For website analysis and browser automation
  - Amazon Nova Pro - For video understanding and classification

- **Frontend**
  - Streamlit - Provides interactive web interfaces
  - VNC Viewer - For remote browser visualization

- **Agent Frameworks**
  - Strands - For building and managing AI agents
  - Model Control Protocol (MCP) - For standardized AI model interaction

- **Browser Automation**
  - Browser-Use - For website interaction and analysis
  - Chrome DevTools Protocol (CDP) - For browser control
  - Playwright - For advanced browser interactions

- **Video Processing**
  - ffmpeg-python - For video file handling and processing
  - OpenCV - For frame extraction and image processing

- **Search and Analysis**
  - Exa API - For website content search and analysis
  - AWS SDK (Boto3) - For AWS service integration

## Installation

### Prerequisites
- Python 3.8+
- Chrome/Chromium browser (for browser automation)
- FFmpeg (for video processing)
- AWS account with access to Bedrock and Nova Pro models
- Docker (optional, for VNC server)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/VerRan/ads_agents_demo.git
cd ads_agents_demo
```

2. Run the installation script:
```bash
python install.py
```

3. Or install dependencies manually:
```bash
pip install -r requirements.txt
cd pre-advertising-analysis-agent
pip install -r requirements.txt
cd ../ads-materials-understand-agent
pip install -r requirements.txt
```

4. Configure AWS credentials:
```bash
aws configure
```

5. Set required environment variables:
```bash
# For Exa API
export API_KEY="your-exa-api-key"

# For AWS (if not using aws configure)
export AWS_ACCESS_KEY_ID="your-aws-access-key"
export AWS_SECRET_ACCESS_KEY="your-aws-secret-key"
export AWS_DEFAULT_REGION="us-east-1"
```

6. Install FFmpeg (if not already installed):
   - **macOS**: `brew install ffmpeg`
   - **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Usage

### Running the Integrated UI

```bash
streamlit run streamlit_ui.py
```

This will launch the combined UI that provides access to all analysis tools.

### Running Individual Modules

#### Pre-Advertising Analysis Agent
```bash
cd pre-advertising-analysis-agent
streamlit run ads_analysis_ui.py
```

#### Ads Materials Understanding Agent
```bash
cd ads-materials-understand-agent
streamlit run app.py
```

### Browser Automation Setup

1. Start Chrome/Chromium with CDP support:
```bash
google-chrome --remote-debugging-port=9222
```

2. Set up VNC server (optional, for remote viewing):
```bash
docker run -p 6081:6081 -p 5901:5901 -d --name vnc-browser dorowu/ubuntu-desktop-lxde-vnc
```

3. Configure CDP connection in the UI:
   - Local connection: `http://localhost:9222`
   - Remote connection: Enter the remote CDP URL
   - VNC URL (if using): `http://localhost:6081/vnc.html`

## Example Workflows

### Website Analysis Workflow

1. Launch the integrated UI
2. Navigate to the "Website Analysis" tab
3. Enter the target website URL
4. Select analysis options (product, competitor, market, audience)
5. Click "Analyze Website"
6. Review the generated analysis report with insights on:
   - Product positioning and pricing strategy
   - Competitive landscape and differentiators
   - Market opportunities and trends
   - Target audience demographics and behavior

### Browser Automation Workflow

1. Start Chrome with remote debugging enabled
2. Launch the integrated UI
3. Navigate to the "Browser Automation" tab
4. Enter the CDP URL (default: http://localhost:9222)
5. Specify the target website URL
6. Enter your analysis instructions
7. Click "Start Browser Automation"
8. Monitor the browser actions in real-time
9. Review the captured screenshots and analysis report

### Video Analysis Workflow

1. Launch the integrated UI
2. Navigate to the "Video Analysis" tab
3. Choose your preferred method (upload, URL, or chat)
4. Provide the video file or URL
5. Initiate the analysis
6. Review the video content understanding and classification results
7. (Optional) Ask follow-up questions about the video content
8. Export or save the analysis results for reporting

## Troubleshooting

### Common Issues

1. **Browser Connection Failures**
   - Ensure Chrome/Chromium is running with remote debugging enabled
   - Verify the CDP URL is correct (default: http://localhost:9222)
   - Check network connections and firewall settings
   - Try restarting the browser with the debugging port
   - Use `curl http://localhost:9222/json/version` to test CDP connectivity

2. **VNC Viewer Issues**
   - Ensure the VNC server is running properly
   - Verify port mappings are correct (default: 6081)
   - Try accessing the VNC URL directly in a new tab
   - Check Docker container status with `docker ps`
   - Restart the VNC container if needed

3. **API Authentication Errors**
   - Ensure EXA_API_KEY environment variable is correctly set
   - Verify AWS credentials are valid and have necessary permissions
   - Check that your AWS account has access to the required models
   - Test AWS connectivity with `aws sts get-caller-identity`

4. **Video Processing Issues**
   - Check that FFmpeg is properly installed with `ffmpeg -version`
   - Ensure video files are in supported formats
   - Verify AWS permissions for accessing Nova Pro model
   - Check temporary directory permissions
   - Try processing a smaller test video first

## Performance Optimization

- For large videos, consider reducing resolution or length before processing
- Use local CDP connections when possible for faster browser automation
- Adjust the number of browser steps based on website complexity
- Consider batch processing for multiple videos
- Use the appropriate AI model tier based on your analysis needs
- Implement caching for frequently analyzed websites or videos
- Monitor AWS usage to optimize costs for AI model calls

## Security Considerations

- Store API keys and credentials securely using environment variables
- Do not hardcode sensitive information in your scripts
- Use appropriate IAM roles and permissions for AWS services
- Be mindful of the websites and videos you analyze, respecting privacy and copyright
- Consider implementing rate limiting for API calls
- Regularly update dependencies to address security vulnerabilities

## Future Enhancements

- Integration with additional AI models for specialized analysis
- Support for more video formats and sources
- Enhanced reporting with data visualization
- API endpoints for programmatic access
- Multi-language support for global marketing analysis
- Integration with popular marketing platforms and analytics tools
- Automated scheduled analysis for ongoing monitoring

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

📊 **Use ADS Agents Demo to drive your advertising decisions with AI-powered insights!**
