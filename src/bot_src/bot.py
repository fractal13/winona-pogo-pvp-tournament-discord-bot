#!/usr/bin/env python3

import interactions
import os
import dotenv
import atexit

def cleanup():
    print("Bot shutting down...")
    # Perform cleanup tasks here (e.g., close database connections)
    print("Bot stopped.")
    return


def main():
    dotenv.load_dotenv()
    TOKEN = os.getenv("BOT_TOKEN")

    client = interactions.Client(token=TOKEN)

    client.load_extension("ping_command")
    client.load_extension("tournament_command")
    client.load_extension("reload_command")

    atexit.register(cleanup)

    client.start()
    return

if __name__ == "__main__":
    main()
