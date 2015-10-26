import os
import bitjws
import alchemyjsonschema as ajs
from alchemyjsonschema.dictify import jsonify
from jsonschema import validate, ValidationError
from flask import Flask, request, current_app, make_response, g
from flask.ext import login
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

from flask_bitjws import Application, get_bitjws_header_payload

from sqlalchemy_login_models.model import User as SLM_User
from model import Coin

import cfg

factory = ajs.SchemaFactory(ajs.AlsoChildrenWalker)

app = Application(__name__)
app._static_folder = "%s/static" % os.path.realpath(os.path.dirname(__file__))


class FlaskUser(SLM_User, login.UserMixin):

    def __init__(self, address, username):
        super(FlaskUser, self).__init__(address=address, username=username)
        self.address = address
        self.username = username


# Setup flask app
app.config['SQLALCHEMY_DATABASE_URI'] = cfg.SA_ENGINE_URI

db = SQLAlchemy(app)
db.register_base(FlaskUser)
db.register_base(Coin)
db.init_app(app)
login_manager = login.LoginManager()
login_manager.init_app(app)


# Custom request authentication based on bitjws.
@login_manager.request_loader
def load_user_from_request(request):
    if not hasattr(request, 'jws_header') or request.jws_header is None:
        # Validation failed.
        return None
    return FlaskUser.query.filter_by(address=str(request.jws_header['kid'])).first()


@app.route('/coin', methods=['GET'])
@login.login_required
def get_coins():
    coinsq = Coin.query.all()
    cschema = factory.__call__(Coin)
    coins = [jsonify(c, cschema) for c in coinsq]
    response = current_app.create_bitjws_response(coins)
    return response

@app.route('/coin', methods=['POST'])
@login.login_required
def post_coin():
    if not hasattr(request, 'jws_header') or request.jws_header is None:
        return "Invalid Payload", 401
    metal = request.jws_payload.get('metal')
    mint = request.jws_payload.get('mint')
    coin = Coin(metal, mint)
    db.session.add(coin)
    try:
        db.session.commit()
    except Exception as ie:
        return generic_code_error('Could not create coin')
    newcoin = jsonify(coin, factory.__call__(coin))
    return current_app.create_bitjws_response(newcoin)


@app.route('/user', methods=['GET'])
@login.login_required
def get_user():
    userdict = jsonify(login.current_user, factory.__call__(login.current_user))
    return current_app.create_bitjws_response(userdict)


@app.route('/user', methods=['POST'])
def post_user():
    if not hasattr(request, 'jws_header') or request.jws_header is None:
        return "Invalid Payload", 401

    username = request.jws_payload.get('username')
    address = request.jws_header['kid']
    user = FlaskUser(address=address, username=username)
    db.session.add(user)
    try:
        db.session.commit()
    except Exception as ie:
        return generic_code_error('username or address taken')
    return current_app.create_bitjws_response(jsonify(user,
                                                      factory.__call__(user)))


if __name__ == "__main__":
    db.create_all(app=app)
    app.run(host='0.0.0.0', port=8002, debug=True)
