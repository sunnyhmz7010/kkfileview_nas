# 1. 使用官方 Python 3.9 作为基础镜像
FROM python:latest

# 2. 设置工作目录
WORKDIR /app

# 3. 复制所有项目文件到容器
COPY . .

# 4. 配置 pip 源为清华镜像，并安装必要依赖
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --upgrade pip && \
    pip install --no-cache-dir flask gunicorn werkzeug jinja2 click itsdangerous markupsafe

# 5. 设置环境变量（可在 `docker run` 传递）
ENV FILE_URL_DATA="localhost"
ENV PREVIEW_URL_DATA="localhost"

# 6. 创建 `/app/files` 目录，并赋予适当权限
RUN mkdir -p /app/files && chmod 777 /app/files

# 7. 设置 Flask 访问的文件路径
ENV FILE_DIR="/app/files"

# 8. 暴露 Flask 运行端口
EXPOSE 5000

# 9. 运行应用（使用 Gunicorn）
CMD ["gunicorn", "--reload", "-w", "2", "-b", "0.0.0.0:5000", "run:app"]
