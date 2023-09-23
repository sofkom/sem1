from appl import app, db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    psw = db.Column(db.String(256), nullable=False)
    salt = db.Column(db.String(128), nullable=False)
    token = db.Column(db.String(256))
    photo = db.Column(db.String(128))
    about = db.Column(db.String(256))


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    data = db.Column(db.DateTime, default = datetime.utcnow)
    us_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'))

class EntryPh(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(64), nullable=False)
    en_id = db.Column(db.Integer, db.ForeignKey('entry.id', ondelete='cascade'))

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    en_id = db.Column(db.Integer, db.ForeignKey('entry.id'))
    us_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    data = db.Column(db.DateTime, default=datetime.utcnow)

class Sub(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    en_id = db.Column(db.Integer, db.ForeignKey('entry.id'))
    us_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    en_id = db.Column(db.Integer, db.ForeignKey('entry.id'))
    us_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Chats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    us_id_1 = db.Column(db.Integer, db.ForeignKey('user.id'))
    us_id_2 = db.Column(db.Integer, db.ForeignKey('user.id'))


class MesText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'))
    us_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    data = db.Column(db.DateTime, default=datetime.utcnow)


# with app.app_context():
#     db.drop_all()
#     db.create_all()