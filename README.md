# Swagger + bitjws Example App

The app is a Coin collection, where Users identified by bitjws keys can create and manage virtual Coins stored on the server. For detailed documentation of the API, see the [swagger spec](http://deginner.github.io/swaxample-ui/).

[Deginner](https://github.com/deginner/) created this app to demo its rapid API development stack. It will be featured in a tutorial and a meetup of that nature. Follow and fork it to participate.


### Deginner Application Stack

| Project |                 Version    |  Description                    |
|---------|------------|---------------|---------------------------------|
|[bitjws](https://github.com/deginner/bitjws) | [![PyPi version](https://img.shields.io/pypi/v/bitjws.svg)](https://pypi.python.org/pypi/bitjws/) |JWS ([JSON Web Signature](http://self-issued.info/docs/draft-ietf-jose-json-web-signature.html)) using Bitcoin message signing as the algorithm.|
|[flask-bitjws](https://github.com/deginner/flask-bitjws) | [![PyPi version](https://img.shields.io/pypi/v/flask-bitjws.svg)](https://pypi.python.org/pypi/flask-bitjws/) |[Flask](http://flask.pocoo.org) extension for [bitjws](https://github.com/g-p-g/bitjws) authentication. |
|[bravado-bitjws](https://github.com/deginner/bravado-bitjws) | [![PyPi version](https://img.shields.io/pypi/v/bravado-bitjws.svg)](https://pypi.python.org/pypi/bravado-bitjws/) |Bravado-bitjws is an add on for [Bravado](https://github.com/Yelp/bravado) that allows [bitjws](https://github.com/g-p-g/bitjws) authentication.|
|[sqlalchemy-login-models](https://github.com/deginner/sqlalchemy-login-models) | 0.0.4 | User related data models for a server using [SQLAlchemy](http://www.sqlalchemy.org/), and [json schemas](http://json-schema.org/). |


### Imported Stack

| Project |                 Version    |  Description                    |
|---------|------------|---------------|---------------------------------|
|[Flask](http://flask.pocoo.org/) | [![PyPi version](https://img.shields.io/pypi/v/flask.svg)](https://pypi.python.org/pypi/flask/) | Flask is a microframework for Python based on Werkzeug, Jinja 2 and good intentions. |
|[Swagger](http://swagger.io/) | 2.0 | Swagxample includes a Swagger spec which is used to configure the [bravado-bitjws](https://github.com/deginner/bravado-bitjws) client automatically. |
|[SQLAlchemy](https://sqlalchemy.org) | [![PyPi version](https://img.shields.io/pypi/v/sqlalchemy.svg)](https://pypi.python.org/pypi/sqlalchemy/) | SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL. |
|[flask-swagger](https://github.com/deginner/flask-swagger) | [![PyPi version](https://img.shields.io/pypi/v/flask-swagger.svg)](https://pypi.python.org/pypi/flask-swagger/) |A Swagger 2.0 spec extractor for Flask. |
|[alchemyjsonchema](https://github.com/deginner/alchemyjsonschema) | [![PyPi version](https://img.shields.io/pypi/v/alchemyjsonschema.svg)](https://pypi.python.org/pypi/alchemyjsonschema/) | Convert SQLAlchemy ORM objects to schemas. |
|[Swagger-UI](http://swagger.io/swagger-ui/) | [![NPM version](https://badge.fury.io/js/swagger-ui.png)](http://badge.fury.io/js/swagger-ui) | Automatically generated, interactive documentation for Swagger specs. |


## Install

By default it's expected that [secp256k1](https://github.com/bitcoin/secp256k1) is available, so install it before proceeding; make sure to run `./configure --enable-module-recovery`. If you're using some other library that provides the functionality necessary for this, check the __Using a custom library__ section of the bitjws README.

##### Building secp256k1

In case you need to install the `secp256k1` C library, the following sequence of commands is recommended. If you already have `secp256k1`, make sure it was compiled from the expected git commit or it might fail to work due to API incompatibilities.

```
git clone git://github.com/bitcoin/secp256k1.git libsecp256k1
cd libsecp256k1
git checkout d7eb1ae96dfe9d497a26b3e7ff8b6f58e61e400a
./autogen.sh
./configure --enable-module-recovery
make
sudo make install
```

## Usage

Start the server in debugging mode.

`python swagxample/server.py`

Start the server using gunicorn, as suitable for a production environment.

`make run`


## Automated Swagger Updates

To update the swagger spec's paths, flask-swagger provides a generator. This can be run with `make swagger`, but it is worth looking at what is happening.

`flaskswagger swagxample.server:app --template swagxample/static/swagger.json --out-dir swagxample/static/`

This crawls the app's routes looking for flask-swagger docstrings. If so, it updates the template and outputs it. In this case, the spec is being edited in place. The net result is that the spec's paths will be updated based on the latest docstrings in your app.

The definitions in this example were also automatically generated, those using [alchemyjsonschema](https://github.com/podhmo/alchemyjsonschema). It's command schema extractor was run on both [sqlalchemy-login-models](https://github.com/deginner/sqlalchemy-login-models) and the SQLAlchemy model(s) in this repo. For example (where $SWAGXAMPLE_APP_HOME is the root of this repo):

`alchemyjsonschema sqlalchemy_login_models.model -s --out-dir $SWAGXAMPLE_APP_HOME/swagxample/static`


## Configuration

This app expects a Python configuration file, which can be specified using the SWAGXAMPLE_CONFIG_FILE environmental variable.

`export SWAGXAMPLE_CONFIG_FILE = /path/to/cfg.py`

The format of the config file is as shown in example_cfg.py. Be sure to change the keys before deploying in production!


## Tests

By exercizing all of the Deginner components in an integrated context, functional completion can be tested, along with complex use cases. For this reason, this example app has more unit tests than strictly necessary, and include use of the relatively heavy (for unit tests) [bravado-bitjws](https://github.com/deginner/bravado-bitjws) client.

Currently the tests expect the server to be running on 0.0.0.0:8002, like the default `make run` behavior. This test method is scheduled for an immediate upgrade.

`python setup.py pytest`
