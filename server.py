import os
import bitjws
from jsonschema import validate, ValidationError
from flask import Flask, jsonify, request, current_app, make_response, g
from flask.ext import login
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

from flask_mrest.models import Model, SuperModel, UserModel, query_to_item
from flask_mrest.errorhandlers import *

from flask_bitjws import Application, get_bitjws_header_payload

from model import db, User, Coin, dictify_item, query_to_item

import cfg

app = Application(__name__)
app._static_folder = "%s/static" % os.path.realpath(os.path.dirname(__file__))

# Setup flask app
app.config['SQLALCHEMY_DATABASE_URI'] = cfg.SA_ENGINE_URI
db.init_app(app)
login_manager = login.LoginManager()
login_manager.init_app(app)


# Custom request authentication based on bitjws.
@login_manager.request_loader
def load_user_from_request(request):
    if not hasattr(request, 'jws_header') or request.jws_header is None:
        # Validation failed.
        return None
    return User.query.filter_by(address=str(request.jws_header['kid'])).first()


@app.route('/coin', methods=['GET'])
@login.login_required
def get_coins():
    coinsq = Coin.query.all()
    coins = query_to_item(coinsq, Coin)
    print coins
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
    return current_app.create_bitjws_response(dictify_item(coin, Coin))


@app.route('/user', methods=['GET'])
@login.login_required
def get_user():
    userdict = dictify_item(login.current_user, User)
    return current_app.create_bitjws_response(userdict)


@app.route('/user', methods=['POST'])
def post_user():
    if not hasattr(request, 'jws_header') or request.jws_header is None:
        return "Invalid Payload", 401

    username = request.jws_payload.get('username')
    address = request.jws_header['kid']
    user = User(address, username)
    db.session.add(user)
    try:
        db.session.commit()
    except Exception as ie:
        return generic_code_error('username or address taken')
    response = current_app.create_bitjws_response(dictify_item(user, User))
    return response


if __name__ == "__main__":
    db.create_all(app=app)
    app.run(host='0.0.0.0', port=8002, debug=True)
