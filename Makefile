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

insert-guilds:
	. $(VENV)/bin/activate; ./main.py cli add-guild --guild-name "Pallet Town PvP" --guild-id "846263191176740942"
	. $(VENV)/bin/activate; ./main.py cli set-admin-channel-id --channel-id "846263191176740942" --guild-id "846263191176740942"
	. $(VENV)/bin/activate; ./main.py cli add-tournament-channel-id --channel-id "952010420158332958" --guild-id "846263191176740942"
	. $(VENV)/bin/activate; ./main.py cli add-guild --guild-name "fractal13's server" --guild-id "870759348505305168"
	. $(VENV)/bin/activate; ./main.py cli set-admin-channel-id --channel-id "992204923926216795" --guild-id "870759348505305168"
	. $(VENV)/bin/activate; ./main.py cli add-tournament-channel-id --channel-id "1365173677666340874" --guild-id "870759348505305168"
