import os
from app import create_app, db
from app.models import User, Role, Post, questionnaire, Permission, Question, Option, Score, NumberControl, RowControl, Relation, questionnaireRelease, questionnaireAnswer, QuestionAnswer
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post, 
                questionnaire=questionnaire, Permission=Permission, 
                Question=Question, Option=Option, Score=Score,
                NumberControl=NumberControl, RowControl=RowControl,
                Relation=Relation,
                questionnaireRelease=questionnaireRelease,
                questionnaireAnswer=questionnaireAnswer,
                QuestionAnswer=QuestionAnswer,
                )

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
