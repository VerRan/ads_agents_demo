# ADS Agents Demo

This repository contains a comprehensive demonstration of AI-powered advertising analysis agents that can process, analyze, and classify advertising data across multiple formats.

## Project Overview

The ADS Agents Demo is a suite of AI-powered tools designed to help marketers and advertising professionals make data-driven decisions. The project consists of two main modules:

1. **Ads Analysis Module**: Focuses on website analysis and advertising strategy development
2. **Video Classification Agent**: Specializes in analyzing and categorizing video content

Together, these modules provide a complete toolkit for understanding and optimizing advertising content across different media formats.

## Project Structure

- `ads_analysis/`: Website and advertising analysis module
  - `ads_analysis_ui.py`: UI for the ads analysis functionality
  - `browser_use/`: Browser automation components
  - `combined_ads_ui.py`: Integrated UI for all analysis tools
  - `browser_use_ui.py`: UI for browser automation features
  - `requirements.txt`: Dependencies for the ads analysis module
  - `combined_requirements.txt`: Complete dependencies for the integrated UI
  - `README.md`: Documentation for the ads_analysis module

- `ads-videos-classify-agent/`: Video content analysis and classification module
  - `agent.py`: Core agent implementation for video analysis
  - `app.py`: Streamlit application entry point
  - `requirements.txt`: Dependencies for the video classification module
  - `README.md`: Documentation for the video classification module
  - `temp/`: Directory for temporary video files
  - `test_data/`: Sample videos for testing
  - `tools_test/`: Utility scripts for testing components

## Key Features

### Ads Analysis Module

- **Website Deep Analysis**
  - Product analysis: Understand product positioning, features, and pricing strategies
  - Competitor analysis: Identify main competitors and compare differences
  - Market analysis: Analyze market size, trends, and opportunities
  - Audience analysis: Study target audience characteristics and behaviors

- **Browser Automation**
  - AI-driven: Uses Amazon Bedrock Claude model to control the browser
  - Real-time visualization: View browser operations through VNC/CDP
  - Flexible configuration: Adjust execution steps and connection parameters
  - Automatic reporting: Generate structured analysis reports
  - Remote CDP support: Connect to remote browser instances

- **Integrated UI**
  - Unified entry point: Integrates website analysis and video classification
  - Multi-mode switching: Seamlessly switch between different analysis modes
  - Result integration: Summarize various analysis results into comprehensive reports
  - Intelligent assistant: Provide conversation-based analysis support
  - Form-based inputs: Easy configuration of analysis parameters

### Video Classification Agent

- **Video Content Understanding**
  - Upload local video files (supports mp4, mov, avi formats)
  - Download and analyze videos via URL
  - Understand video content using Amazon Nova Pro
  - Automatically classify videos into 278 predefined categories
  - Display detailed classification results
  - User-friendly interface with video preview

- **Multiple Analysis Methods**
  - File upload: Analyze locally stored videos
  - URL analysis: Process videos from web sources
  - Chat-based analysis: Interact with the agent through conversation
  - Batch processing: Handle multiple videos sequentially

## Technology Stack

- **AI Models**
  - Amazon Bedrock (Claude 3.7 Sonnet) - For website analysis and browser automation
  - Amazon Nova Pro - For video understanding and classification

- **Frontend**
  - Streamlit - Provides interactive web interfaces
  - VNC Viewer - For remote browser visualization

- **Agent Frameworks**
  - Strands - For building and managing AI agents

- **Browser Automation**
  - Browser-Use - For website interaction and analysis
  - Chrome DevTools Protocol (CDP) - For browser control

- **Video Processing**
  - ffmpeg-python - For video file handling and processing

- **Search and Analysis**
  - Exa API - For website content search and analysis

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

2. Set up the Ads Analysis module:
```bash
cd ads_analysis
pip install -r combined_requirements.txt
```

3. Set up the Video Classification Agent:
```bash
cd ../ads-videos-classify-agent
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

## Usage

### Running the Integrated UI

```bash
cd ads_analysis
python run_combined_ui.py
```

This will launch the combined UI that provides access to both website analysis and video classification features.

### Running the Video Classification Agent Separately

```bash
cd ads-videos-classify-agent
streamlit run app.py
```

The video classification application will be available at http://localhost:8501

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

## Example Workflows

### Website Analysis Workflow

1. Launch the integrated UI
2. Navigate to the "Website Analysis" tab
3. Enter the target website URL
4. Select analysis options (product, competitor, market, audience)
5. Click "Analyze Website"
6. Review the generated analysis report

### Video Classification Workflow

1. Launch the video classification agent
2. Choose your preferred method (upload, URL, or chat)
3. Provide the video file or URL
4. Initiate the analysis
5. Review the video content understanding and classification results
6. (Optional) Ask follow-up questions about the video content

## Troubleshooting

### Common Issues

1. **Browser Connection Failures**
   - Ensure Chrome/Chromium is running with remote debugging enabled
   - Verify the CDP URL is correct (default: http://localhost:9222)
   - Check network connections and firewall settings
   - Try restarting the browser with the debugging port

2. **VNC Viewer Issues**
   - Ensure the VNC server is running properly
   - Verify port mappings are correct (default: 6081)
   - Try accessing the VNC URL directly in a new tab
   - Check Docker container status with `docker ps`

3. **API Authentication Errors**
   - Ensure EXA_API_KEY environment variable is correctly set
   - Verify AWS credentials are valid and have necessary permissions
   - Check that your AWS account has access to the required models

4. **Video Processing Issues**
   - Check that FFmpeg is properly installed
   - Ensure video files are in supported formats
   - Verify AWS permissions for accessing Nova Pro model
   - Check temporary directory permissions

## Performance Optimization

- For large videos, consider reducing resolution or length before processing
- Use local CDP connections when possible for faster browser automation
- Adjust the number of browser steps based on website complexity
- Consider batch processing for multiple videos

## Future Enhancements

- Integration with additional AI models for specialized analysis
- Support for more video formats and sources
- Enhanced reporting with data visualization
- API endpoints for programmatic access
- Multi-language support for global marketing analysis

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
