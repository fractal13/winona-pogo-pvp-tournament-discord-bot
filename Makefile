VENV := .virtual_environment

all: install

$(VENV):
	python3 -m venv $(VENV)

install: install-deb install-pip

install-deb:
	for package in libsqlite3-dev python3.12-venv gcc python3-dev; do \
		dpkg -l | egrep '^ii *'$${package}' ' 2>&1 > /dev/null || sudo apt install $${package}; \
	done

install-pip: $(VENV)
	. $(VENV)/bin/activate; pip3 install -U -r requirements.txt

launch-bot:
	. $(VENV)/bin/activate; ./main.py bot

create-db:
	$(MAKE) -C external all
	. $(VENV)/bin/activate; ./main.py cli create-pokemon-db
	. $(VENV)/bin/activate; ./main.py cli create-user-db
	. $(VENV)/bin/activate; ./main.py cli create-guild-db
