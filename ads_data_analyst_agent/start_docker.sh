#!/bin/bash

# Docker容器启动脚本
# 同时启动Streamlit和FastAPI服务

echo "🚀 启动AI数据分析师服务..."

# 启动FastAPI服务 (后台运行)
echo "🔗 启动REST API服务..."
uvicorn api_server:app --host 0.0.0.0 --port 8000 &
API_PID=$!

# 等待API服务启动
sleep 3

# 启动Streamlit服务 (前台运行)
echo "🌐 启动Streamlit Web界面..."
streamlit run demo_app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false &
STREAMLIT_PID=$!

echo "✅ 服务启动完成！"
echo "📱 Streamlit Web界面: http://localhost:8501"
echo "🔗 REST API服务: http://localhost:8000"
echo "📚 API文档: http://localhost:8000/docs"

# 等待任一服务退出
wait -n

# 清理进程
echo "🛑 正在停止服务..."
kill $API_PID 2>/dev/null
kill $STREAMLIT_PID 2>/dev/null

echo "✅ 服务已停止"