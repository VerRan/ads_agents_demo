from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
import traceback
import json
from ads_go_agent_as_tool import (
    coordinator_agent,
    product_analyst,
    competitor_analyst,
    market_analyst,
    audience_analyst,
    run_agent_graph
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'ads-go-agent-api'
    }), 200

# Main analysis endpoint
@app.route('/api/v1/analyze', methods=['POST'])
def analyze_product():
    """
    Main product analysis endpoint
    
    Request Body:
    {
        "url": "https://example.com",
        "analysis_type": "comprehensive" | "quick",
        "language": "zh" | "en"
    }
    
    Response:
    {
        "status": "success" | "error",
        "data": {
            "analysis_result": "...",
            "timestamp": "...",
            "analysis_id": "..."
        },
        "message": "..."
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'Request body is required'
            }), 400
        
        url = data.get('url')
        if not url:
            return jsonify({
                'status': 'error',
                'message': 'URL is required'
            }), 400
        
        analysis_type = data.get('analysis_type', 'comprehensive')
        language = data.get('language', 'zh')
        
        # Create analysis task
        task = f"分析一下{url}" if language == 'zh' else f"Analyze {url}"
        
        # Run the coordinator agent
        logger.info(f"Starting analysis for URL: {url}")
        result = coordinator_agent(task)
        
        analysis_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return jsonify({
            'status': 'success',
            'data': {
                'analysis_result': str(result),
                'timestamp': datetime.now().isoformat(),
                'analysis_id': analysis_id,
                'url': url,
                'analysis_type': analysis_type
            },
            'message': 'Analysis completed successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Error in analyze_product: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': f'Analysis failed: {str(e)}'
        }), 500

# Product analysis endpoint
@app.route('/api/v1/analyze/product', methods=['POST'])
def analyze_product_only():
    """
    Product-specific analysis endpoint
    
    Request Body:
    {
        "query": "product name or URL"
    }
    """
    try:
        data = request.get_json()
        query = data.get('query')
        
        if not query:
            return jsonify({
                'status': 'error',
                'message': 'Query is required'
            }), 400
        
        result = product_analyst(query)
        
        return jsonify({
            'status': 'success',
            'data': {
                'product_analysis': str(result),
                'timestamp': datetime.now().isoformat()
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in analyze_product_only: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Competitor analysis endpoint
@app.route('/api/v1/analyze/competitor', methods=['POST'])
def analyze_competitor():
    """
    Competitor analysis endpoint
    
    Request Body:
    {
        "query": "product name or URL"
    }
    """
    try:
        data = request.get_json()
        query = data.get('query')
        
        if not query:
            return jsonify({
                'status': 'error',
                'message': 'Query is required'
            }), 400
        
        result = competitor_analyst(query)
        
        return jsonify({
            'status': 'success',
            'data': {
                'competitor_analysis': str(result),
                'timestamp': datetime.now().isoformat()
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in analyze_competitor: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Market analysis endpoint
@app.route('/api/v1/analyze/market', methods=['POST'])
def analyze_market():
    """
    Market analysis endpoint
    
    Request Body:
    {
        "query": "product name or URL"
    }
    """
    try:
        data = request.get_json()
        query = data.get('query')
        
        if not query:
            return jsonify({
                'status': 'error',
                'message': 'Query is required'
            }), 400
        
        result = market_analyst(query)
        
        return jsonify({
            'status': 'success',
            'data': {
                'market_analysis': str(result),
                'timestamp': datetime.now().isoformat()
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in analyze_market: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Audience analysis endpoint
@app.route('/api/v1/analyze/audience', methods=['POST'])
def analyze_audience():
    """
    Audience analysis endpoint
    
    Request Body:
    {
        "query": "product name or URL"
    }
    """
    try:
        data = request.get_json()
        query = data.get('query')
        
        if not query:
            return jsonify({
                'status': 'error',
                'message': 'Query is required'
            }), 400
        
        result = audience_analyst(query)
        
        return jsonify({
            'status': 'success',
            'data': {
                'audience_analysis': str(result),
                'timestamp': datetime.now().isoformat()
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in analyze_audience: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Agent graph endpoint
@app.route('/api/v1/analyze/graph', methods=['POST'])
def analyze_with_graph():
    """
    Analysis using agent graph topology
    
    Request Body:
    {
        "task": "analysis task description"
    }
    """
    try:
        data = request.get_json()
        task = data.get('task')
        
        if not task:
            return jsonify({
                'status': 'error',
                'message': 'Task is required'
            }), 400
        
        result = run_agent_graph(task)
        
        return jsonify({
            'status': 'success',
            'data': {
                'graph_analysis': str(result),
                'timestamp': datetime.now().isoformat()
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in analyze_with_graph: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Batch analysis endpoint
@app.route('/api/v1/analyze/batch', methods=['POST'])
def batch_analyze():
    """
    Batch analysis endpoint for multiple URLs
    
    Request Body:
    {
        "urls": ["https://example1.com", "https://example2.com"],
        "analysis_types": ["product", "market", "competitor", "audience"]
    }
    """
    try:
        data = request.get_json()
        urls = data.get('urls', [])
        analysis_types = data.get('analysis_types', ['product'])
        
        if not urls:
            return jsonify({
                'status': 'error',
                'message': 'URLs list is required'
            }), 400
        
        results = []
        
        for url in urls:
            url_results = {}
            
            for analysis_type in analysis_types:
                try:
                    if analysis_type == 'product':
                        result = product_analyst(url)
                    elif analysis_type == 'competitor':
                        result = competitor_analyst(url)
                    elif analysis_type == 'market':
                        result = market_analyst(url)
                    elif analysis_type == 'audience':
                        result = audience_analyst(url)
                    else:
                        result = f"Unknown analysis type: {analysis_type}"
                    
                    url_results[analysis_type] = str(result)
                    
                except Exception as e:
                    url_results[analysis_type] = f"Error: {str(e)}"
            
            results.append({
                'url': url,
                'analyses': url_results
            })
        
        return jsonify({
            'status': 'success',
            'data': {
                'batch_results': results,
                'timestamp': datetime.now().isoformat(),
                'total_urls': len(urls)
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in batch_analyze: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# API documentation endpoints
@app.route('/docs', methods=['GET'])
@app.route('/api/docs', methods=['GET'])
def api_docs_html():
    """HTML API documentation endpoint"""
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ads Go Agent REST API 文档</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
            h2 { color: #34495e; margin-top: 30px; }
            h3 { color: #7f8c8d; }
            .endpoint { background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #3498db; }
            .method { display: inline-block; padding: 4px 8px; border-radius: 3px; font-weight: bold; margin-right: 10px; }
            .get { background: #27ae60; color: white; }
            .post { background: #e74c3c; color: white; }
            pre { background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px; overflow-x: auto; }
            code { background: #ecf0f1; padding: 2px 4px; border-radius: 3px; }
            .example { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; }
            .status-badge { display: inline-block; padding: 2px 6px; border-radius: 3px; font-size: 12px; }
            .success { background: #d4edda; color: #155724; }
            .error { background: #f8d7da; color: #721c24; }
            table { width: 100%; border-collapse: collapse; margin: 15px 0; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Ads Go Agent REST API 文档</h1>
            <p><strong>版本:</strong> 1.0.0</p>
            <p><strong>基础URL:</strong> <code>http://localhost:5000</code></p>
            <p><strong>描述:</strong> 基于多智能体系统的广告分析REST API，提供产品、竞品、市场和受众分析功能。</p>

            <h2>📋 API 端点总览</h2>
            <table>
                <tr><th>方法</th><th>端点</th><th>描述</th></tr>
                <tr><td><span class="method get">GET</span></td><td>/health</td><td>健康检查</td></tr>
                <tr><td><span class="method post">POST</span></td><td>/api/v1/analyze</td><td>综合分析</td></tr>
                <tr><td><span class="method post">POST</span></td><td>/api/v1/analyze/product</td><td>产品分析</td></tr>
                <tr><td><span class="method post">POST</span></td><td>/api/v1/analyze/competitor</td><td>竞品分析</td></tr>
                <tr><td><span class="method post">POST</span></td><td>/api/v1/analyze/market</td><td>市场分析</td></tr>
                <tr><td><span class="method post">POST</span></td><td>/api/v1/analyze/audience</td><td>受众分析</td></tr>
                <tr><td><span class="method post">POST</span></td><td>/api/v1/analyze/graph</td><td>智能体图分析</td></tr>
                <tr><td><span class="method post">POST</span></td><td>/api/v1/analyze/batch</td><td>批量分析</td></tr>
                <tr><td><span class="method get">GET</span></td><td>/docs</td><td>API文档 (本页面)</td></tr>
                <tr><td><span class="method get">GET</span></td><td>/api/v1/docs</td><td>JSON格式文档</td></tr>
            </table>

            <h2>🔍 详细端点说明</h2>

            <div class="endpoint">
                <h3><span class="method get">GET</span> /health</h3>
                <p>检查API服务状态</p>
                <div class="example">
                    <strong>响应示例:</strong>
                    <pre>{
  "status": "healthy",
  "timestamp": "2025-01-07T10:30:00.000Z",
  "service": "ads-go-agent-api"
}</pre>
                </div>
            </div>

            <div class="endpoint">
                <h3><span class="method post">POST</span> /api/v1/analyze</h3>
                <p>执行综合产品分析，调用所有可用的分析智能体</p>
                <div class="example">
                    <strong>请求体:</strong>
                    <pre>{
  "url": "https://www.kreadoai.com/",
  "analysis_type": "comprehensive",
  "language": "zh"
}</pre>
                    <strong>参数说明:</strong>
                    <ul>
                        <li><code>url</code> (必需): 要分析的网站URL</li>
                        <li><code>analysis_type</code> (可选): "comprehensive" 或 "quick"，默认 "comprehensive"</li>
                        <li><code>language</code> (可选): "zh" 或 "en"，默认 "zh"</li>
                    </ul>
                </div>
            </div>

            <div class="endpoint">
                <h3><span class="method post">POST</span> /api/v1/analyze/product</h3>
                <p>专门的产品特征分析</p>
                <div class="example">
                    <strong>请求体:</strong>
                    <pre>{
  "query": "https://www.kreadoai.com/"
}</pre>
                </div>
            </div>

            <div class="endpoint">
                <h3><span class="method post">POST</span> /api/v1/analyze/competitor</h3>
                <p>竞争对手和竞争格局分析</p>
                <div class="example">
                    <strong>请求体:</strong>
                    <pre>{
  "query": "https://www.kreadoai.com/"
}</pre>
                </div>
            </div>

            <div class="endpoint">
                <h3><span class="method post">POST</span> /api/v1/analyze/market</h3>
                <p>市场趋势、规模和机会分析</p>
                <div class="example">
                    <strong>请求体:</strong>
                    <pre>{
  "query": "https://www.kreadoai.com/"
}</pre>
                </div>
            </div>

            <div class="endpoint">
                <h3><span class="method post">POST</span> /api/v1/analyze/audience</h3>
                <p>目标受众和用户画像分析</p>
                <div class="example">
                    <strong>请求体:</strong>
                    <pre>{
  "query": "https://www.kreadoai.com/"
}</pre>
                </div>
            </div>

            <div class="endpoint">
                <h3><span class="method post">POST</span> /api/v1/analyze/batch</h3>
                <p>批量分析多个URL</p>
                <div class="example">
                    <strong>请求体:</strong>
                    <pre>{
  "urls": [
    "https://www.kreadoai.com/",
    "https://example.com/"
  ],
  "analysis_types": ["product", "market", "competitor", "audience"]
}</pre>
                </div>
            </div>

            <h2>🧪 测试示例</h2>
            <div class="example">
                <h3>使用 cURL 测试:</h3>
                <pre># 健康检查
curl -X GET http://localhost:5000/health

# 产品分析
curl -X POST http://localhost:5000/api/v1/analyze/product \\
  -H "Content-Type: application/json" \\
  -d '{"query": "https://www.kreadoai.com/"}'

# 综合分析
curl -X POST http://localhost:5000/api/v1/analyze \\
  -H "Content-Type: application/json" \\
  -d '{
    "url": "https://www.kreadoai.com/",
    "analysis_type": "comprehensive",
    "language": "zh"
  }'</pre>
            </div>

            <h2>📊 响应格式</h2>
            <div class="example">
                <h3>成功响应:</h3>
                <pre>{
  "status": "success",
  "data": {
    "analysis_result": "分析结果...",
    "timestamp": "2025-01-07T10:30:00.000Z",
    "analysis_id": "analysis_20250107_103000"
  },
  "message": "Analysis completed successfully"
}</pre>

                <h3>错误响应:</h3>
                <pre>{
  "status": "error",
  "message": "错误描述"
}</pre>
            </div>

            <h2>🚀 快速开始</h2>
            <div class="example">
                <pre># 1. 安装依赖
pip install -r requirements_api.txt

# 2. 启动API服务器
python ads_go_agent_rest_api.py

# 3. 测试API
python test_api.py</pre>
            </div>

            <h2>📝 状态码</h2>
            <table>
                <tr><th>状态码</th><th>说明</th></tr>
                <tr><td>200</td><td><span class="status-badge success">成功</span></td></tr>
                <tr><td>400</td><td><span class="status-badge error">请求错误 (缺少必需参数)</span></td></tr>
                <tr><td>404</td><td><span class="status-badge error">端点不存在</span></td></tr>
                <tr><td>500</td><td><span class="status-badge error">服务器内部错误</span></td></tr>
            </table>

            <footer style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; color: #7f8c8d;">
                <p>📧 如有问题，请联系开发团队</p>
                <p>🔄 最后更新: 2025-01-07</p>
            </footer>
        </div>
    </body>
    </html>
    """
    return html_content

@app.route('/api/v1/docs', methods=['GET'])
def api_docs_json():
    """JSON API documentation endpoint"""
    docs = {
        'title': 'Ads Go Agent REST API',
        'version': '1.0.0',
        'description': 'REST API for advertising analysis using multi-agent system',
        'base_url': 'http://localhost:5000',
        'endpoints': {
            'GET /health': {
                'description': 'Health check endpoint',
                'parameters': None,
                'response_example': {
                    'status': 'healthy',
                    'timestamp': '2025-01-07T10:30:00.000Z',
                    'service': 'ads-go-agent-api'
                }
            },
            'POST /api/v1/analyze': {
                'description': 'Main comprehensive analysis endpoint',
                'parameters': {
                    'url': 'string (required) - URL to analyze',
                    'analysis_type': 'string (optional) - comprehensive or quick',
                    'language': 'string (optional) - zh or en'
                },
                'request_example': {
                    'url': 'https://www.kreadoai.com/',
                    'analysis_type': 'comprehensive',
                    'language': 'zh'
                }
            },
            'POST /api/v1/analyze/product': {
                'description': 'Product-specific analysis',
                'parameters': {
                    'query': 'string (required) - Product name or URL'
                },
                'request_example': {
                    'query': 'https://www.kreadoai.com/'
                }
            },
            'POST /api/v1/analyze/competitor': {
                'description': 'Competitor analysis',
                'parameters': {
                    'query': 'string (required) - Product name or URL'
                },
                'request_example': {
                    'query': 'https://www.kreadoai.com/'
                }
            },
            'POST /api/v1/analyze/market': {
                'description': 'Market analysis',
                'parameters': {
                    'query': 'string (required) - Product name or URL'
                },
                'request_example': {
                    'query': 'https://www.kreadoai.com/'
                }
            },
            'POST /api/v1/analyze/audience': {
                'description': 'Audience analysis',
                'parameters': {
                    'query': 'string (required) - Product name or URL'
                },
                'request_example': {
                    'query': 'https://www.kreadoai.com/'
                }
            },
            'POST /api/v1/analyze/graph': {
                'description': 'Analysis using agent graph',
                'parameters': {
                    'task': 'string (required) - Analysis task description'
                },
                'request_example': {
                    'task': '分析一下https://www.kreadoai.com/'
                }
            },
            'POST /api/v1/analyze/batch': {
                'description': 'Batch analysis for multiple URLs',
                'parameters': {
                    'urls': 'array (required) - List of URLs to analyze',
                    'analysis_types': 'array (optional) - Types of analysis to perform'
                },
                'request_example': {
                    'urls': ['https://www.kreadoai.com/', 'https://example.com/'],
                    'analysis_types': ['product', 'market', 'competitor', 'audience']
                }
            }
        },
        'response_format': {
            'success': {
                'status': 'success',
                'data': '...',
                'message': '...'
            },
            'error': {
                'status': 'error',
                'message': '...'
            }
        },
        'status_codes': {
            '200': 'Success',
            '400': 'Bad Request (missing required parameters)',
            '404': 'Not Found (endpoint does not exist)',
            '500': 'Internal Server Error'
        }
    }
    
    return jsonify(docs), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)