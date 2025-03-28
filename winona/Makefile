VENV := ../.virtual_environment

all:
	@echo HELLO

initialize_database: tournament_database.db

tournament_database.db: \
	create_user_database.py \
	ingest_pokemon_list.py ../external/pvpoke/src/data/gamemaster/pokemon.json
	. $(VENV)/bin/activate; ./create_user_database.py $@
	. $(VENV)/bin/activate; ./ingest_pokemon_list.py $@

test-pokemon-from-database:
	. $(VENV)/bin/activate; ./commands.py tournament_database.db

test-tournament:
	. $(VENV)/bin/activate; ./tournament.py
test-user:
	. $(VENV)/bin/activate; ./user.py



../external/pvpoke/src/data/gamemaster/pokemon.json:
	make -C ../external pvpoke
