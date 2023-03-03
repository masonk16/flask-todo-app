import os
from flask import Flask
from flask_login import LoginManager
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
SECRET_KEY = os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    tasks = db.relationship('TaskItem', backref='owner')

    def __repr__(self):
        return f'User{self.first_name}{self.email}'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(255))
    due_date = db.Column(db.DateTime())
    status = db.Column(db.String(255))
    task_owner = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Task{self.task_name}{self.due_date}'


app.app_context().push()
db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
