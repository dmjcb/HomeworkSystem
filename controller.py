import datetime
import random
import os, zipfile

from models import *

dir = '信1701-3班-报表-7月6日'


def zip_file():
    # 压缩文件夹
    startdir = os.path.join(os.getcwd(), dir)
    file_news = dir + '.zip'
    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(startdir, '')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            z.write(os.path.join(dirpath, filename), fpath + filename)
    z.close()


# 根据学号获取文件路径
def get_file_path(num):
    folder_path = os.path.join(os.getcwd(), dir)
    for i in os.listdir(folder_path):
        if num in i:
            # 返回对应文件的绝对路径
            return os.path.join(folder_path, i)


def get_time():
    return datetime.datetime.now()


# 获取所有学生学号
def get_all_num():
    stu = session.query(Stu).all()
    id_list = [i.id for i in stu]
    return id_list


# 生成随机编码
def get_random_id():
    alphabet = 'abcdefghijklmnopqrstuvwxyz123456'
    chars = random.sample(alphabet, 5)
    return ''.join(chars)


# 获取某次作业已经上传的学生学号
def get_uploaded_stu(work_id):
    people = session.query(Record).filter(work_id=work_id).all()
    res = []
    for i in people:
        res.append(i.stu_id)
    return res


# 添加作业
def add_new_work(data):
    while (True):
        random_id = get_random_id()
        # 查询该编码是否可用
        if find_work(random_id) is False:
            break
    name, classes, amount = data.values()
    work = Work(id=random_id, name=name, classes=classes, amount=amount, time=get_time())
    session.add(work)
    session.commit()
    session.close()


def find_work(id):
    res = session.query(Work).get(id)
    return res[0] if res else False


def find_record(id):
    res = session.query(Record).get(id)
    return res[0] if res else False


# 添加上传记录
def add_upload_record(data):
    work_id, stu_id = data.values()
    while (True):
        random_id = get_random_id()
        # 查询该编码是否可用
        if find_record(random_id) is False:
            break
    record = Record(id=random_id, work_id=work_id, stu_id=stu_id, time=get_time())
    session.add(record)
    session.commit()
    session.close()


# 获得未完成作业的情况
def get_work_info():
    return session.query(Work).filter(Work.status == 'no').all()
