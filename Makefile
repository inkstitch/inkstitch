dist: *.py *.inx inkstitch-venv
	zip -r inkstitch-$$(git tag -l | grep ^v | tail -n 1)-$$(uname)-$$(uname -m).zip *.py *.inx inkstitch-venv

inkstitch-venv: requirements.txt
	rm -rf inkstitch-venv
	virtualenv inkstitch-venv
	source inkstitch-venv/bin/activate \
	pip install -r requirements.txt \
    for file in inkstitch-venv/lib/python*/site-packages/wx/_*.so; do patchelf --set-rpath '$$ORIGIN'; done
