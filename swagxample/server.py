import alchemyjsonschema as ajs
import bitjws
import copy
import imp
import os
import sys
import sqlalchemy as sa
import sqlalchemy.orm as orm
from alchemyjsonschema.dictify import jsonify
from jsonschema import validate, ValidationError
from flask import Flask, request, current_app, make_response, g
from flask.ext.login import login_required, current_user
from flask_bitjws import FlaskBitjws, load_jws_from_request, FlaskUser
from sqlalchemy_login_models.model import UserKey, User as SLM_User
from model import Coin

try:
    cfg_loc = os.environ.get('SWAGXAMPLE_CONFIG_FILE', 'example_cfg.py')
    cfg_raw = None
    with open(cfg_loc, 'r') as f:
        cfg = imp.load_module("config_as_module", f, cfg_loc,
                              ('.py', 'r', imp.PY_SOURCE))
except Exception as e:
    print e
    print "Unable to configurate application. Exiting."
    sys.exit()

factory = ajs.SchemaFactory(ajs.AlsoChildrenWalker)


__all__ = ['app', ]


def get_last_nonce(app, key, nonce):
    """
    Get the last_nonce used by the given key from the SQLAlchemy database.
    Update the last_nonce to nonce at the same time.

    :param str key: the public key the nonce belongs to
    :param int nonce: the last nonce used by this key
    """
    uk = ses.query(UserKey).filter(UserKey.key==key)\
            .filter(UserKey.last_nonce<nonce * 1000).first()
    if not uk:
        return None
    lastnonce = copy.copy(uk.last_nonce)
    # TODO Update DB record in same query as above, if possible
    uk.last_nonce = nonce * 1000
    try:
        ses.commit()
    except Exception as e:
        print e
        ses.rollback()
        ses.flush()
    return lastnonce


def get_user_by_key(app, key):
    """
    An SQLAlchemy User getting function. Get a user by public key.

    :param str key: the public key the user belongs to
    """
    user = ses.query(SLM_User).join(UserKey).filter(UserKey.key==key).first()
    return user


# Setup flask app and FlaskBitjws
app = Flask(__name__)
app._static_folder = "%s/static" % os.path.realpath(os.path.dirname(__file__))
FlaskBitjws(app, privkey=cfg.PRIV_KEY, get_last_nonce=get_last_nonce,
            get_user_by_key=get_user_by_key)

# Setup database
eng = sa.create_engine(cfg.SA_ENGINE_URI)
ses = orm.sessionmaker(bind=eng)()
SLM_User.metadata.create_all(eng)
UserKey.metadata.create_all(eng)
Coin.metadata.create_all(eng)

# A dynamic way to initialize the models
#for m in model.__all__:
#    if m != 'FlaskUser':
#        getattr(model, m).metadata.create_all(eng)

@app.route('/coin', methods=['GET'])
@login_required
def get_coins():
    coinsq = ses.query(Coin).all()
    if not coinsq:
        return None
    cschema = factory.__call__(Coin)
    coins = [jsonify(c, cschema) for c in coinsq]
    response = current_app.bitjws.create_response(coins)
    return response


@app.route('/coin', methods=['POST'])
@login_required
def post_coin():
    metal = request.jws_payload['data'].get('metal')
    mint = request.jws_payload['data'].get('mint')
    coin = Coin(metal, mint, current_user.id)
    ses.add(coin)
    try:
        ses.commit()
    except Exception as ie:
        return generic_code_error('Could not create coin')
    newcoin = jsonify(coin, factory.__call__(coin))
    return current_app.bitjws.create_response(newcoin)


@app.route('/user', methods=['GET'])
@login_required
def get_user():
    userdict = jsonify(current_user, factory.__call__(current_user))
    return current_app.bitjws.create_response(userdict)


@app.route('/user', methods=['POST'])
def post_user():
    load_jws_from_request(request)
    if not hasattr(request, 'jws_header') or request.jws_header is None:
        return "Invalid Payload", 401
    username = request.jws_payload['data'].get('username')
    address = request.jws_header['kid']
    user = SLM_User(username=username)
    ses.add(user)
    try:
        ses.commit()
    except Exception as ie:
        print ie
        ses.rollback()
        ses.flush()
        return 'username taken', 400
    userkey = UserKey(key=address, keytype='public', user_id=user.id,
                      last_nonce=request.jws_payload['iat']*1000)
    ses.add(userkey)
    try:
        ses.commit()
    except Exception as ie:
        print ie
        ses.rollback()
        ses.flush()
        #ses.delete(user)
        #ses.commit()
        return 'username taken', 400
    jresult = jsonify(userkey, factory.__call__(userkey))
    return current_app.bitjws.create_response(jresult)


@app.route('/userkey', methods=['GET'])
@login_required
def get_userkey():
    username = request.jws_payload['data'].get('username')
    address = request.jws_header['kid']
    userkeys = jsonify(current_user, factory.__call__(current_user))
    return current_app.bitjws.create_response(userdict)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8002, debug=True)

