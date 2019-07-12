from flask_sqlalchemy import SQLAlchemy
from main import app

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    channel = db.Column(db.String(100), primary_key=True)
    alarm_time = db.Column(db.Integer)
    message = db.Column(db.String(100), default='no message')
    location = db.Column(db.String(100), default='no location')
    set_new_alarm = db.Column(db.Boolean, default=False)  # 매일매일 false 로 바뀌며 새롭게 알람 시간을 설정했으면 true로 바뀐다. false일 경우 전날 시간으로 알람 메세지 전송
    step = db.Column(db.Integer, default=-1)
    talk_subject = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'{self.channel} {self.alarm_time} {self.message} {self.location}'

