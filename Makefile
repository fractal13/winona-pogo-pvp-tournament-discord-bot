VENV := .virtual_environment

all: install

$(VENV):
	python3 -m venv $(VENV)

install: install-deb install-pip

install-deb:
	dpkg -l | egrep '^ii *libsqlite3-dev' 2>&1 > /dev/null || sudo apt install libsqlite3-dev

install-pip: $(VENV)
	. $(VENV)/bin/activate; pip3 install -r requirements.txt


