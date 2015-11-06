build:
	flaskswagger swagxample.server:app --template swagxample/static/swagger.json --out-dir swagxample/static/
	python setup.py build

install:
	python setup.py install

clean:
	rm -rf .cache build dist *.egg-info test/__pycache__
	rm -rf test/*.pyc *.egg *~ *pyc test/*~ .eggs

swagger:
	flaskswagger swagxample.server:app --template swagxample/static/swagger.json --out-dir swagxample/static/

run:
	gunicorn gunicorn_app:gunicorn_app -b 0.0.0.0:8002

