FROM python:3.12-slim

WORKDIR /app

# 安装 Node.js 用于构建前端
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 安装后端依赖
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r backend/requirements.txt

# 复制前端并构建
COPY frontend/ ./frontend/
RUN cd frontend && npm install && npm run build && \
    cp -r dist ../backend/static

# 复制后端代码
COPY backend/ ./backend/

WORKDIR /app/backend

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
