source bin/activate

pip3 install -r requirements.txt

如果没有创建数据库请输入命令

python manage.py shell

然后输入

db.create_all()

创建数据库

python manage.py runserver  --host=0.0.0.0 --port=80

