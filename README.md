source bin/activate

pip3 install -r requirements.txt

python manage.py runserver  --host=0.0.0.0 --port=80

运行程序，程序中已创建数据库

可以输入邮箱clmiao@zju.edu.cn以及密码1234567来登陆


如果没有创建数据库请输入命令

python manage.py shell

然后输入

db.create_all()

创建数据库
