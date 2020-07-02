import os
import time

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        name = request.form.get('name')
        num = request.form.get('num')
        # classes = request.form.get('classes')
        # 获取文件格式
        file_format = f.filename.split('.')[1]
        new_name = '%s-%s-课程设计工作日报表.%s' % (num, name, file_format)
        f.filename = new_name
        # 上传文件所在路径
        upload_path = os.path.join(os.getcwd(), '信1701-3班-报表-7月3日', f.filename)
        # 将路径转换为绝对路径
        upload_path = os.path.abspath(upload_path)
        f.save(upload_path)
        return render_template('success.html', filename=f.filename)
    return render_template('index.html')

# 显示上传信息
@app.route('/info')
def display_upload_info():
    data = get_upload_info()
    return render_template('info.html', data=data,num=len(data))


# 获取文件修改时间
def get_upload_time(path):
    times = os.path.getmtime(path)
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(times))


def get_upload_info():
    data = []
    folder_path = os.path.join(os.getcwd(), '信1701-3班-报表-7月3日')
    for i in os.listdir(folder_path):
        path = os.path.join(folder_path, i)
        if os.path.isfile(path):
            info = {
                'name': i,
                'time': get_upload_time(path)
            }
            data.append(info)
    return data


if __name__ == '__main__':
    app.run()
