FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

RUN echo "deb http://mirrors.aliyun.com/debian buster main" > /etc/apt/sources.list && echo "deb http://mirrors.aliyun.com/debian-security buster/updates main" >>/etc/apt/sources.list && echo "deb http://mirrors.aliyun.com/debian buster-updates main" >>/etc/apt/sources.list

RUN apt-get update -y && apt-get upgrade -y && apt-get install ssh -y && apt-get install vim -y

RUN pip install  --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple/  --trusted-host pypi.tuna.tsinghua.edu.cn -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]