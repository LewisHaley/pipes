PYTHON_VER := python3.12

check: \
	autoformat \
	lint \
	tests \
	;
.PHONY: check

autoformat: venv
	$</bin/python -m black \
		src \
		tests \
	;
.PHONY: autoformat

lint: venv
	$</bin/python -m pylint \
		src \
		tests \
	;
.PHONY: lint

tests: venv
	$</bin/python -m pytest \
		tests \
	;
.PHONY: tests

venv: venv/pyvenv.cfg
venv/pyvenv.cfg: bootstrap
	bootstrap/bin/python -m venv --upgrade-deps venv
	venv/bin/python -m pip install \
		--prefer-binary \
		--require-virtualenv \
		--progress-bar=off \
		--quiet \
		--report - \
		--requirement=requirements.txt \
	;

requirements.txt: bootstrap
	$</bin/python -m piptools compile \
		--output-file=$@ \
		--extra=dev \
		pyproject.toml \
	;

bootstrap: bootstrap/pyvenv.cfg
bootstrap/pyvenv.cfg:
	/usr/bin/$(PYTHON_VER) -m venv --upgrade-deps bootstrap
	bootstrap/bin/python -m pip install \
		--prefer-binary \
		--require-virtualenv \
		--progress-bar=off \
		--quiet \
		--report - \
		wheel==0.42.0 \
		setuptools==69.0.2 \
		pip==23.3.2 \
		pip-tools==7.3.0 \
	;

clean:
	rm -rf \
		bootstrap \
		venv \
	;
.PHONY: \
	clean
