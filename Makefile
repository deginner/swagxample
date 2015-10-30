build:
	python setup.py build

install:
	python setup.py install

clean:
	rm -rf build dist swagxample.egg-info test/__pycache__
	rm -rf test/*.pyc *.egg *~ *pyc test/*~

run:
	gunicorn gunicorn_app:gunicorn_app -b 0.0.0.0:8002

