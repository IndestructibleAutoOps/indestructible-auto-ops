FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY src/ ./src/
COPY configs/ ./configs/

# 创建数据目录
RUN mkdir -p /data /cache

# 设置环境变量
ENV PYTHONPATH=/app/src
ENV LOG_LEVEL=info
ENV FOLDING_STRATEGY=hybrid-folding
ENV VECTOR_DIMENSIONS=768

# 暴露端口
EXPOSE 8080 9090 9091

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health', timeout=5)"

# 运行应用
CMD ["python", "-m", "src.semantic_folding.engine"]