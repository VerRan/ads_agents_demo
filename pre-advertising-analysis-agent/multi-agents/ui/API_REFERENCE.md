# Ads Go Agent REST API Reference

## Overview
This REST API provides access to a multi-agent advertising analysis system that can analyze products, competitors, markets, and audiences for advertising purposes.

## Base URL
```
http://localhost:5000
```

## Authentication
Currently, no authentication is required for this API.

## Endpoints

### Health Check
**GET** `/health`

Check if the API service is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-07T10:30:00.000Z",
  "service": "ads-go-agent-api"
}
```

### Comprehensive Analysis
**POST** `/api/v1/analyze`

Perform a comprehensive analysis of a product/website using all available agents.

**Request Body:**
```json
{
  "url": "https://www.kreadoai.com/",
  "analysis_type": "comprehensive",
  "language": "zh"
}
```

**Parameters:**
- `url` (required): The URL to analyze
- `analysis_type` (optional): "comprehensive" or "quick" (default: "comprehensive")
- `language` (optional): "zh" or "en" (default: "zh")

**Response:**
```json
{
  "status": "success",
  "data": {
    "analysis_result": "Detailed analysis result...",
    "timestamp": "2025-01-07T10:30:00.000Z",
    "analysis_id": "analysis_20250107_103000",
    "url": "https://www.kreadoai.com/",
    "analysis_type": "comprehensive"
  },
  "message": "Analysis completed successfully"
}
```

### Product Analysis
**POST** `/api/v1/analyze/product`

Analyze product features, positioning, and characteristics.

**Request Body:**
```json
{
  "query": "https://www.kreadoai.com/"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "product_analysis": "Product analysis result...",
    "timestamp": "2025-01-07T10:30:00.000Z"
  }
}
```

### Competitor Analysis
**POST** `/api/v1/analyze/competitor`

Analyze competitors and competitive landscape.

**Request Body:**
```json
{
  "query": "https://www.kreadoai.com/"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "competitor_analysis": "Competitor analysis result...",
    "timestamp": "2025-01-07T10:30:00.000Z"
  }
}
```

### Market Analysis
**POST** `/api/v1/analyze/market`

Analyze market trends, size, and opportunities.

**Request Body:**
```json
{
  "query": "https://www.kreadoai.com/"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "market_analysis": "Market analysis result...",
    "timestamp": "2025-01-07T10:30:00.000Z"
  }
}
```

### Audience Analysis
**POST** `/api/v1/analyze/audience`

Analyze target audience and user demographics.

**Request Body:**
```json
{
  "query": "https://www.kreadoai.com/"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "audience_analysis": "Audience analysis result...",
    "timestamp": "2025-01-07T10:30:00.000Z"
  }
}
```

### Agent Graph Analysis
**POST** `/api/v1/analyze/graph`

Perform analysis using the agent graph topology (star configuration).

**Request Body:**
```json
{
  "task": "分析一下https://www.kreadoai.com/"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "graph_analysis": "Graph analysis result...",
    "timestamp": "2025-01-07T10:30:00.000Z"
  }
}
```

### Batch Analysis
**POST** `/api/v1/analyze/batch`

Analyze multiple URLs with specified analysis types.

**Request Body:**
```json
{
  "urls": [
    "https://www.kreadoai.com/",
    "https://example.com/"
  ],
  "analysis_types": ["product", "market", "competitor", "audience"]
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "batch_results": [
      {
        "url": "https://www.kreadoai.com/",
        "analyses": {
          "product": "Product analysis...",
          "market": "Market analysis...",
          "competitor": "Competitor analysis...",
          "audience": "Audience analysis..."
        }
      }
    ],
    "timestamp": "2025-01-07T10:30:00.000Z",
    "total_urls": 2
  }
}
```

### API Documentation
**GET** `/api/v1/docs`

Get API documentation in JSON format.

## Error Responses

All endpoints return error responses in the following format:

```json
{
  "status": "error",
  "message": "Error description"
}
```

**Common HTTP Status Codes:**
- `200`: Success
- `400`: Bad Request (missing required parameters)
- `404`: Not Found (endpoint doesn't exist)
- `500`: Internal Server Error

## Usage Examples

### cURL Examples

**Health Check:**
```bash
curl -X GET http://localhost:5000/health
```

**Comprehensive Analysis:**
```bash
curl -X POST http://localhost:5000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.kreadoai.com/",
    "analysis_type": "comprehensive",
    "language": "zh"
  }'
```

**Product Analysis:**
```bash
curl -X POST http://localhost:5000/api/v1/analyze/product \
  -H "Content-Type: application/json" \
  -d '{
    "query": "https://www.kreadoai.com/"
  }'
```

### Python Example

```python
import requests
import json

# Comprehensive analysis
url = "http://localhost:5000/api/v1/analyze"
data = {
    "url": "https://www.kreadoai.com/",
    "analysis_type": "comprehensive",
    "language": "zh"
}

response = requests.post(url, json=data)
result = response.json()

if result["status"] == "success":
    print("Analysis completed:")
    print(result["data"]["analysis_result"])
else:
    print("Error:", result["message"])
```

### JavaScript Example

```javascript
// Using fetch API
const analyzeProduct = async (url) => {
  try {
    const response = await fetch('http://localhost:5000/api/v1/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        url: url,
        analysis_type: 'comprehensive',
        language: 'zh'
      })
    });
    
    const result = await response.json();
    
    if (result.status === 'success') {
      console.log('Analysis completed:', result.data.analysis_result);
    } else {
      console.error('Error:', result.message);
    }
  } catch (error) {
    console.error('Request failed:', error);
  }
};

// Usage
analyzeProduct('https://www.kreadoai.com/');
```

## Running the API

1. Install dependencies:
```bash
pip install -r requirements_api.txt
```

2. Run the development server:
```bash
python ads_go_agent_rest_api.py
```

3. For production, use gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 ads_go_agent_rest_api:app
```

## Rate Limiting

Currently, no rate limiting is implemented. Consider adding rate limiting for production use.

## CORS

CORS is enabled for all origins. Adjust the CORS configuration for production security requirements.

## Logging

The API logs all requests and errors. Check the console output for debugging information.