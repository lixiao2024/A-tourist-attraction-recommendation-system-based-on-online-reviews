FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制后端代码
COPY 后端/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY 后端/ .

# 创建上传目录
RUN mkdir -p uploads

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "simple_app:app", "--host", "0.0.0.0", "--port", "8000"] 