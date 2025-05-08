VENV := .virtual_environment

all: install

$(VENV):
	python3 -m venv $(VENV)

install: install-deb install-pip

install-deb:
	dpkg -l | egrep '^ii *libsqlite3-dev' 2>&1 > /dev/null || sudo apt install libsqlite3-dev
	dpkg -l | egrep '^ii *python3.12-venv' 2>&1 > /dev/null || sudo apt install python3.12-venv
	dpkg -l | egrep '^ii *gcc ' 2>&1 > /dev/null || sudo apt install gcc
	dpkg -l | egrep '^ii *python3-dev ' 2>&1 > /dev/null || sudo apt install python3-dev
install-pip: $(VENV)
	. $(VENV)/bin/activate; pip3 install -U -r requirements.txt

launch-bot:
	. $(VENV)/bin/activate; ./main.py bot

