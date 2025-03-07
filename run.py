from flask import Flask, render_template, send_from_directory
import os
import json
import base64

app = Flask(__name__)

# 读取环境变量
file_url_data = os.getenv("FILE_URL_DATA", "http://localhost")
preview_url_data = os.getenv("PREVIEW_URL_DATA", "http://localhost")

# file_url_data = '192.168.10.25:5000'
# preview_url_data = '192.168.10.28:8012'

# 设定文件目录（默认是 `/app/files`）
FILE_DIR = os.getenv("FILE_DIR", "/app/files")
# FILE_DIR = 'files'

# 生成 kkFileView 预览链接
def generate_preview_url(file_path):
    """ 生成 kkFileView 预览链接 """
    file_url = f"http://{file_url_data}/file/{file_path}"  # 注意这里直接拼接完整路径
    encoded_url = base64.b64encode(file_url.encode('utf-8')).decode('utf-8')  # Base64 编码
    preview_url = f"http://{preview_url_data}/onlinePreview?url={encoded_url}"  # 预览链接
    return preview_url

# 注册 `generate_preview_url` 到 Jinja2 模板
@app.context_processor
def utility_processor():
    return dict(generate_preview_url=generate_preview_url)

# 首页：列出文件和目录
@app.route('/')
def index():
    def build_file_structure(directory):
        """ 递归构建文件和文件夹结构 """
        structure = {}
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                structure[item] = build_file_structure(item_path)  # 递归处理子目录
            else:
                structure[item] = os.path.relpath(item_path, FILE_DIR)  # 返回相对路径
        return structure

    file_structure = build_file_structure(FILE_DIR)  # 递归读取文件结构
    return render_template('index.html', file_structure=file_structure)

# 允许访问次级目录中的文件
@app.route('/file/<path:filename>')
def download_file(filename):
    """ 允许访问 `files/` 目录下的次级文件 """
    return send_from_directory(FILE_DIR, filename)

# 启动 Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
