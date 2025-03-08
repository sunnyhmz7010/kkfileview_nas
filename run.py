import os
import base64
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# 读取环境变量
file_url_data = os.getenv("FILE_URL_DATA", "http://localhost")
preview_url_data = os.getenv("PREVIEW_URL_DATA", "http://localhost")

# file_url_data = '192.168.10.25:5000'
# preview_url_data = '192.168.10.28:8012'

# 设定文件目录（Windows 和 Linux 兼容）
FILE_DIR = os.getenv("FILE_DIR", os.path.abspath("files"))  # 默认 `files/` 目录
# FILE_DIR = 'files'

# 生成 kkFileView 预览链接（修正 Windows 路径）
def generate_preview_url(file_path):
    """ 生成 kkFileView 预览链接，统一使用 / 作为路径分隔符 """
    file_path = file_path.replace("\\", "/")  # 统一路径格式
    file_url = f"http://{file_url_data}/file/{file_path}"  # 生成 Flask 访问路径
    encoded_url = base64.b64encode(file_url.encode('utf-8')).decode('utf-8')  # Base64 编码
    preview_url = f"http://{preview_url_data}/onlinePreview?url={encoded_url}"  # kkFileView 预览链接
    return preview_url

# 注册模板全局函数
@app.context_processor
def utility_processor():
    return dict(generate_preview_url=generate_preview_url)

# 递归构建文件和文件夹结构，兼容 Windows
def build_file_structure(directory):
    """ 递归构建文件夹结构，Windows/Linux 兼容 """
    structure = {}
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            structure[item] = build_file_structure(item_path)  # 递归处理子目录
        else:
            relative_path = os.path.relpath(item_path, FILE_DIR).replace("\\", "/")  # 修正路径格式
            structure[item] = relative_path  # 返回相对路径
    return structure

# 首页：列出文件和目录
@app.route('/')
def index():
    file_structure = build_file_structure(FILE_DIR)  # 递归读取文件结构
    return render_template('index.html', file_structure=file_structure)

# 允许访问次级目录中的文件
@app.route('/file/<path:filename>')
def download_file(filename):
    """ 允许访问 `files/` 目录下的次级文件 """
    safe_filename = filename.replace("\\", "/")  # 兼容 Windows 路径
    return send_from_directory(FILE_DIR, safe_filename)

# 启动 Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
