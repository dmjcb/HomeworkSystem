import json

from flask import Flask, render_template, request, send_from_directory
from controller import *

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


# 存储上传的文件
@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method != 'POST':
        return
    f = request.files['file']
    name = request.form.get('name')
    num = request.form.get('num')
    work_id = request.form.get('num')
    # 获取文件格式
    file_format = f.filename.split('.')[1]
    # 按老师要求命名
    new_name = '%s-%s-课程设计工作日报表.%s' % (num, name, file_format)
    f.filename = new_name
    # 上传文件的所在路径
    upload_path = os.path.join(os.getcwd(), dir, f.filename)
    # 将路径转换为绝对路径
    upload_path = os.path.abspath(upload_path)
    f.save(upload_path)

    # 添加提交记录

    return json.dumps({"result": 1})


# 下载文件
@app.route('/download/', methods=['GET'])
def download():
    zip_file()
    path = os.path.join(os.getcwd())
    return send_from_directory(path, dir + '.zip', as_attachment=True)


@app.route('/admin', methods=['GET'])
def admin():
    work_info = get_work_info()
    return render_template('admin.html', work_info=work_info)


if __name__ == '__main__':
    app.run()
