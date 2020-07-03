import os
import time

from flask import Flask, render_template, request, redirect, url_for
import models
app = Flask(__name__)


@app.route('/')
def hello_world():
    data = get_upload_info()
    num1 = len(get_stu_num())
    return render_template('index.html', data=data, num1=num1)


# 存储上传的文件
@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        name = request.form.get('name')
        num = request.form.get('num')
        # 获取文件格式
        file_format = f.filename.split('.')[1]
        # 按老师要求命名
        new_name = '%s-%s-课程设计工作日报表.%s' % (num, name, file_format)
        f.filename = new_name
        # 上传文件的所在路径
        upload_path = os.path.join(os.getcwd(), '信1701-3班-报表-7月3日', f.filename)
        # 将路径转换为绝对路径
        upload_path = os.path.abspath(upload_path)
        f.save(upload_path)
        return redirect(url_for('hello_world'))


# 根据学号获取文件路径
def get_file_path(num):
    folder_path = os.path.join(os.getcwd(), '信1701-3班-报表-7月3日')
    for i in os.listdir(folder_path):
        if num in i:
            # 返回对应文件的绝对路径
            return os.path.join(folder_path, i)


# 获取文件修改时间
def get_upload_time(num):
    path = get_file_path(num)
    times = os.path.getmtime(path)
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(times))


# 获取已经上传学生的学号
def get_stu_num():
    data = []
    folder_path = os.path.join(os.getcwd(), '信1701-3班-报表-7月3日')
    for i in os.listdir(folder_path):
        path = os.path.join(folder_path, i)
        if os.path.isfile(path):
            num, name, file_format = i.split('-')
            data.append(num)
    return data


def get_upload_info():
    data2 = []
    num_info = get_stu_num()
    for i in models.stu_info:
        info = {
            'status': 'no',
            'num': i['num'],
            'name': i['name'],
            'time': '-----'
        }
        # 若该人已经提交
        if num_info and i['num'] in num_info:
            info['status'] = 'yes'
            info['time'] = get_upload_time(i['num'])
        data2.append(info)
    return data2


if __name__ == '__main__':
    app.run()
