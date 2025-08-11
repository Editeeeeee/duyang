# 使用官方 Python 3.8 镜像作为基础镜像
FROM python:3.8-slim

# 设置工作目录为 /app
WORKDIR /app

# 复制当前目录的所有内容到 /app 目录
COPY . /app

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 公开 Flask 默认的 5000 端口
EXPOSE 5000

# 设置环境变量，避免每次运行时询问
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# 启动 Flask 应用
CMD ["flask", "run", "--host=0.0.0.0"]
