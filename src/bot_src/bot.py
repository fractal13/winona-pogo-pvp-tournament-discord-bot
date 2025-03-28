#!/usr/bin/env python3

import interactions
import os
import dotenv
import atexit


dotenv.load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

client = interactions.Client(token=TOKEN)

client.load_extension("ping_command")
client.load_extension("tournament_command")
client.load_extension("reload_command")

def cleanup():
    print("Bot shutting down...")
    # Perform cleanup tasks here (e.g., close database connections)
    print("Bot stopped.")
    return

atexit.register(cleanup)

client.start()
