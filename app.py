import json
import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# 定义文件存储路径
DATA_FILE = 'data.json'

# 确保数据文件存在，如果没有则创建一个空的文件
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)  # 初始化为空列表


# 读取 JSON 文件中的所有帖子
def read_data():
    if os.path.getsize(DATA_FILE) == 0:  # 检查文件大小是否为0
        return []  # 如果文件为空，返回一个空列表
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


# 写入数据到 JSON 文件
def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# 首页显示所有的图片和留言
@app.route('/')
def index():
    posts = read_data()  # 读取文件中的所有帖子
    return render_template('index.html', posts=posts)

# 上传图片和留言
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    message = request.form['message']

    # 检查文件是否存在
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join('static/uploads', filename))

        # 获取当前时间
        post_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 获取当前所有的帖子
        posts = read_data()

        # 创建一个新帖
        new_post = {
            'image': filename,
            'message': message,
            'nickname': '匿名',
            'avatar': 'https://example.com/avatar.jpg',
            'time': post_time
        }

        # 添加新帖子到文件
        posts.append(new_post)
        write_data(posts)

    return redirect(url_for('index'))

# 判断文件是否是允许上传的格式
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)
