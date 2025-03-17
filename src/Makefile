VENV := ../.virtual_environment

all:
	@echo HELLO

initialize_database: pokemon_database.db

pokemon_database.db: ./ingest_pokemon_list.py ../external/pvpoke/src/data/gamemaster/pokemon.json
	. $(VENV)/bin/activate; ./ingest_pokemon_list.py

../external/pvpoke/src/data/gamemaster/pokemon.json:
	make -C ../external pvpoke

test-pokemon:
	. $(VENV)/bin/activate; ./commands.py
test-tournament:
	. $(VENV)/bin/activate; ./tournament.py

