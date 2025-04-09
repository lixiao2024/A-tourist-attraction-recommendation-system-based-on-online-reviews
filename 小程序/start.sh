#!/bin/bash

# 显示欢迎信息
echo "====================================================="
echo "  基于在线评论的旅游景点智能推荐系统 - Docker启动脚本"
echo "====================================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "错误: Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 检查Docker服务是否运行
if ! docker info &> /dev/null; then
    echo "错误: Docker服务未运行，请先启动Docker服务"
    exit 1
fi

# 启动服务
echo "正在启动服务..."
docker-compose up -d

# 检查服务是否成功启动
if [ $? -ne 0 ]; then
    echo "错误: 服务启动失败"
    exit 1
fi

echo "服务已成功启动!"
echo ""
echo "后端API服务: http://localhost:8000"
echo "Ollama服务: http://localhost:11434"
echo ""
echo "正在检查Qwen模型是否已安装..."

# 检查Qwen模型是否已安装
if ! docker exec $(docker ps -q -f name=ollama) ollama list | grep -q "shiroi/qwen7b-q4"; then
    echo "Qwen模型未安装，正在拉取..."
    echo "注意: 拉取模型可能需要一些时间，请耐心等待"
    docker exec $(docker ps -q -f name=ollama) ollama pull shiroi/qwen7b-q4:latest
    if [ $? -ne 0 ]; then
        echo "错误: 模型拉取失败"
        exit 1
    fi
    echo "Qwen模型已成功安装!"
else
    echo "Qwen模型已安装，无需再次拉取"
fi

echo ""
echo "====================================================="
echo "  服务已成功启动，您可以开始使用系统了!"
echo "====================================================="
echo ""
echo "如需停止服务，请运行: docker-compose down"
echo "" 