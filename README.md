###NovBlog

由Flask和MongoDb构建的简单博客网站，运行在Python3.5下。

#### 1.如何在本地运行NovBlog

1）克隆代码到本地

`$ git clone https://github.com/Eliefly/NovBlog.git`



2）构建python3虚拟环境，这样不致污染本机环境，并激活虚拟环境

`$ virtualenv --python=python3 venv`

`$ source ./venv/bin/activate`



3）安装依赖的扩展包

`$ pip install -r requirements.txt`



4）安装MongoDb数据库

本人使用的是Ubuntu 16.04，安装参见：[How to Install and Configure MongoDB on Ubuntu 16.04](https://www.howtoforge.com/tutorial/install-mongodb-on-ubuntu-16.04/)



5）运行Flask程序，如下就可在浏览器通过http://127.0.0.1:5000/ 访问NovBlog

```

$ python manage.py runserver

 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

 * Restarting with stat

 * Debugger is active!

 * Debugger pin code: 196-078-756

```

#### 2.将NovBlog部署在腾讯云上，可访问http://139.199.191.60/ 查看（主机到期可能挂掉。。）

部署过程：[腾讯云Unubtu 16.04 （gunicorn+supervisor+ngnix+mongodb）部署Flask应用](http://www.cnblogs.com/elie/p/6341680.html)



















