import os
from app import create_app, db
from app.models import User, Role, Post, Questionaire, Permission, Question, Option, Score, QuestionaireRelease, QuestionaireAnswer, QuestionAnswer
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post, 
                Questionaire=Questionaire, Permission=Permission, 
                Question=Question, Option=Option, Score=Score,
                QuestionaireRelease=QuestionaireRelease,
                QuestionaireAnswer=QuestionaireAnswer,
                QuestionAnswer=QuestionAnswer,
                )

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
