PYTHON := $(shell which python || echo python)
NPM := $(shell which npm || echo npm)
JAVAC := $(shell which javac || echo javac)
JAVA := $(shell which java || echo java)

.PHONY: all deps test run-python run-ts run-java clean

all: deps test

deps: python-deps ts-deps

python-deps:
	$(PYTHON) -m pip install --user -r requirements.txt

ts-deps:
	cd examples/typescript && $(NPM) install

test:
	$(PYTHON) -m pytest -q

run-python:
	$(PYTHON) examples/proxy_python.py

run-python-cache:
	$(PYTHON) examples/proxy_python_cache.py

run-ts:
	cd examples/typescript && npx ts-node proxy.ts

java-build:
	$(JAVAC) -d examples/java examples/java/ProxyExample.java

run-java: java-build
	$(JAVA) -cp examples/java ProxyExample

clean:
	rm -rf examples/typescript/dist examples/java/*.class examples/java/*.d
