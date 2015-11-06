build:
	if ! [ -d "~/.swagxample" ]; \
	then \
		mkdir ~/.swagxample; \
	fi
	python setup.py build

install:
	if ! [ -d "~/.swagxample" ]; \
	then \
		mkdir ~/.swagxample; \
	fi
	python setup.py install

clean:
	rm -rf .cache build dist *.egg-info test/__pycache__
	rm -rf test/*.pyc *.egg *~ *pyc test/*~ .eggs
	rm -rf ~/.swagxample/*

swagger:
	flaskswagger swagxample.server:app --template swagxample/static/swagger.json --out-dir swagxample/static/

