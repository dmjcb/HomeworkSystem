import datetime
import json
import os

import time
import zipfile
import smtplib
from email import encoders

from email.mime.base import MIMEBase
from email.mime.text import MIMEText
# email 用于构建邮件内容
from email.header import Header
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import models

app = Flask(__name__)

dir = '信1701-3班-报表-7月5日'


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
        upload_path = os.path.join(os.getcwd(), dir, f.filename)
        # 将路径转换为绝对路径
        upload_path = os.path.abspath(upload_path)
        f.save(upload_path)
        print(upload_path)
        return json.dumps({"result": 1})


def zip_file():
    # 压缩文件夹
    startdir = os.path.join(os.getcwd(), dir)
    file_news = dir + '.zip'
    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(startdir, '')  # 这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            z.write(os.path.join(dirpath, filename), fpath + filename)
    z.close()


# 下载文件
@app.route('/download/', methods=['GET'])
def download():
    zip_file()
    path = os.path.join(os.getcwd())
    return send_from_directory(path, dir + '.zip', as_attachment=True)


# 根据学号获取文件路径
def get_file_path(num):
    folder_path = os.path.join(os.getcwd(), dir)
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
    folder_path = os.path.join(os.getcwd(), dir)
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


@app.route('/send')
def send_email():
    # 发信方的信息：发信邮箱，QQ 邮箱授权码
    from_addr = '1061299112@qq.com'
    password = 'rihqoamwelwbbfcj'

    # 收信方邮箱
    to_addr = '1061299112@qq.com'

    # 发信服务器
    smtp_server = 'smtp.qq.com'

    curr_time = datetime.datetime.now()
    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    message = '信1701-3班' + curr_time.strftime("%Y-%m-%d") + '课程设计工作日报表'
    msg = MIMEText(message, 'plain', 'utf-8')

    # 邮件头信息
    msg['From'] = Header(from_addr)
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header(message)
    # 添加附件
    zip_file()
    with open(os.path.join(os.getcwd(), dir + '.zip'), 'w') as f:
        # 这里附件的MIME和文件名，这里是xls类型
        mime = MIMEBase('zip', 'zip', filename=dir + '.zip')
        # 用Base64编码
        encoders.encode_base64(mime)
        msg.attach(mime)

    # 开启发信服务，这里使用的是加密传输
    server = smtplib.SMTP_SSL(smtp_server)
    server.connect(smtp_server, 465)
    # 登录发信邮箱
    server.login(from_addr, password)
    # 发送邮件
    server.sendmail(from_addr, to_addr, msg.as_string())
    # 关闭服务器
    server.quit()
    return '发送成功'


if __name__ == '__main__':
    app.run()
