from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext import login

db = SQLAlchemy()


#TODO these database functions don't really belong here...
def dictify_item(item, model):
    columns = [c.name for c in model.__table__.columns]
    columnitems = dict([(c, getattr(item, c)) for c in columns])
    return columnitems


def query_to_item(query, model):
    if isinstance(query, db.Model):
        return dictify_item(query, model)
    else:
        items = []
        for item in query:
            items.append(dictify_item(item, model))
        return items


# SQLAlchemy models
class User(db.Model, login.UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(80), unique=True)

    def __init__(self, address, username):
        self.address = address
        self.username = username


class Coin(db.Model):
    id = db.Column(db.Integer, primary_key=True, doc="primary key")
    metal = db.Column(db.String(255), nullable=False)
    mint = db.Column(db.String(255), nullable=False)

    def __init__(self, metal, mint):
        self.metal = metal
        self.mint = mint
