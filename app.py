import os
import time

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def hello_world():
    data = get_upload_info()
    num1 = len(get_stu_num())
    num2 = 37 - num1
    return render_template('index.html', data=data, num1=num1, num2=num2)


@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        name = request.form.get('name')
        num = request.form.get('num')
        # 获取文件格式
        file_format = f.filename.split('.')[1]
        new_name = '%s-%s-课程设计工作日报表.%s' % (num, name, file_format)
        f.filename = new_name
        # 上传文件所在路径
        upload_path = os.path.join(os.getcwd(), '信1701-3班-报表-7月3日', f.filename)
        # 将路径转换为绝对路径
        upload_path = os.path.abspath(upload_path)
        f.save(upload_path)
        return redirect(url_for('hello_world'))


# 根据学号获取文件路径
def get_file_path(num):
    folder_path = os.path.join(os.getcwd(), '信1701-3班-报表-7月3日')
    for i in os.listdir(folder_path):
        # 文件绝对路径
        path = os.path.join(folder_path, i)
        if os.path.isfile(path):
            nums = i.split('-')[0]
            if num == nums:
                return path


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
        print(path)
        if os.path.isfile(path):
            num, name, file_format = i.split('-')
            print("---", num, name, file_format)
            data.append(num)
    return data


def get_upload_info():
    data = [
        {'num': '20153442', 'name': '李孟凯'},
        {'num': '20163468', 'name': '张振威'},
        {'num': '20173420', 'name': '张焕德'},
        {'num': '20173430', 'name': '王浩然'},
        {'num': '20173434', 'name': '张  帅'},
        {'num': '20173439', 'name': '周成博'},
        {'num': '20173449', 'name': '都博睿'},
        {'num': '20173462', 'name': '王子函'},
        {'num': '20173471', 'name': '刘光磊'},
        {'num': '20173479', 'name': '赵东健'},
        {'num': '20173482', 'name': '封柔昕'},
        {'num': '20173489', 'name': '李兴洲'},
        {'num': '20173496', 'name': '王仁月'},
        {'num': '20173501', 'name': '高  洋'},
        {'num': '20173512', 'name': '郭振璇'},
        {'num': '20173525', 'name': '安寅生'},
        {'num': '20173532', 'name': '王亚杰'},
        {'num': '20173535', 'name': '赵月超'},
        {'num': '20173540', 'name': '韩春雨'},
        {'num': '20173545', 'name': '郝铭杨'},
        {'num': '20173554', 'name': '薄阳瑜'},
        {'num': '20173578', 'name': '刘勤清'},
        {'num': '20173589', 'name': '王晓英'},
        {'num': '20173605', 'name': '郑雪鹏'},
        {'num': '20173616', 'name': '于世超'},
        {'num': '20173631', 'name': '牛少康'},
        {'num': '20173637', 'name': '李泰格'},
        {'num': '20173641', 'name': '陈恒哲'},
        {'num': '20173650', 'name': '赵浩然'},
        {'num': '20173653', 'name': '李元昊'},
        {'num': '20173656', 'name': '许丽娇'},
        {'num': '20173663', 'name': '崔世杰'},
        {'num': '20173669', 'name': '武伟康'},
        {'num': '20173678', 'name': '历  浩'},
        {'num': '20173689', 'name': '莫雨昊'},
        {'num': '20173695', 'name': '姚  燕'},
        {'num': '20173942', 'name': '刘宇琦'}
    ]
    data2 = []
    num_info = get_stu_num()
    print("num :", num_info)
    for i in data:
        info = {'status': 'no', 'num': i['num'], 'name': i['name'], 'time': '-----'}
        # 查询该人是否已经提交
        if num_info and i['num'] in num_info:
            info['status'] = 'yes'
            info['time'] = get_upload_time(i['num'])
        data2.append(info)
    return data2


if __name__ == '__main__':
    app.run()
