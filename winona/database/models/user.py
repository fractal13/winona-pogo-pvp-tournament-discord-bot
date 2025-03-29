#!/usr/bin/env python3

from typing import Optional
from ..database_manager import DatabaseManager
import sys

class User:
    """
    Represents a user with Discord and Pokémon Go accounts.
    """

    def __init__(self, 
                 discord_name: str, 
                 discord_name_in_server: str, 
                 discord_id: int, 
                 pogo_trainer_name: str, 
                 pogo_trainer_code: str, 
                 timezone: str, 
                 user_id: Optional[int] = None, 
                 db_manager: DatabaseManager = None):
        """
        Initializes a User object.

        Args:
            discord_name (str): The user's full Discord name.
            discord_name_in_server (str): The user's nickname in the Discord server.
            discord_id (int): The user's Discord ID.
            pogo_trainer_name (str): The user's Pokémon Go trainer name.
            pogo_trainer_code (str): The user's Pokémon Go trainer code.
            timezone (str): The user's preferred timezone.
            user_id (int, optional): The user's ID in the database. Defaults to None.
            db_manager (DatabaseManager, optional): The database manager instance. 
                                                    Defaults to None.
        """
        self.discord_name = discord_name
        self.discord_name_in_server = discord_name_in_server
        self.discord_id = discord_id
        self.pogo_trainer_name = pogo_trainer_name
        self.pogo_trainer_code = pogo_trainer_code
        self.timezone = timezone
        self.user_id = user_id
        self.db_manager = db_manager

    def save(self):
        """
        Saves the user data to the database.
        """
        if self.user_id:
            # Update existing user
            sql = """
            UPDATE users 
            SET discord_name = ?, discord_name_in_server = ?, discord_id = ?, 
                pogo_trainer_name = ?, pogo_trainer_code = ?, timezone = ? 
            WHERE id = ?
            """
            params = (self.discord_name, self.discord_name_in_server, self.discord_id, 
                      self.pogo_trainer_name, self.pogo_trainer_code, self.timezone, 
                      self.user_id)
        else:
            # Create new user
            sql = """
            INSERT INTO users (discord_name, discord_name_in_server, discord_id, 
                               pogo_trainer_name, pogo_trainer_code, timezone) 
            VALUES (?, ?, ?, ?, ?, ?)
            """
            params = (self.discord_name, self.discord_name_in_server, self.discord_id, 
                      self.pogo_trainer_name, self.pogo_trainer_code, self.timezone)
        
        self.db_manager.execute(sql, params)
        if not self.user_id:
            # Get the inserted user ID
            self.user_id = self.db_manager.cursor.lastrowid

    @classmethod
    def get_by_discord_id(cls, discord_id, db_manager):
        """
        Retrieves a User object from the database by Discord ID.

        Args:
            discord_id (int): The Discord ID of the user.
            db_manager (DatabaseManager): The database manager instance.

        Returns:
            A User object if found, otherwise None.
        """
        sql = "SELECT * FROM users WHERE discord_id = ?"
        row = db_manager.fetchone(sql, (discord_id,))
        if row:
            return cls(*row[1:], user_id=row[0], db_manager=db_manager)
        return None

    def delete(self):
        """
        Deletes the user from the database.
        """
        if self.user_id:
            sql = "DELETE FROM users WHERE id = ?"
            self.db_manager.execute(sql, (self.user_id,))
            self.user_id = None

    @classmethod
    def create_users_table(cls, db_manager):
        """
        Creates the 'users' table in the database.
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            discord_name TEXT NOT NULL,
            discord_name_in_server TEXT,
            discord_id INTEGER UNIQUE NOT NULL,
            pogo_trainer_name TEXT,
            pogo_trainer_code TEXT,
            timezone TEXT
        );
        """
        db_manager.create_table(create_table_sql)

    def __repr__(self):
        """
        Returns a string representation of the User object.
        """
        return f"<User discord_name='{self.discord_name}' discord_id='{self.discord_id}'>"

def main(argv):

    # Example usage (assuming you have a `DatabaseManager` instance)
    db_manager = DatabaseManager("my_database.db") 

    # Create the users table
    User.create_users_table(db_manager)

    # Create two users
    user1 = User(
        "JohnDoe#1234", 
        "John", 
        123456789, 
        "TrainerJohn", 
        "ABCDEFG", 
        "EST", 
        db_manager=db_manager
    )
    user1.save()

    user2 = User(
        "JaneDoe#5678", 
        "Jane", 
        987654321, 
        "TrainerJane", 
        "HIJKLMN", 
        "PST", 
        db_manager=db_manager
    )
    user2.save()

    # Retrieve user1 by Discord ID
    retrieved_user1 = User.get_by_discord_id(123456789, db_manager)
    print(retrieved_user1)  # Output: <User discord_name='JohnDoe#1234' discord_id='123456789'>

    # Update user1's timezone
    retrieved_user1.timezone = "CST"
    retrieved_user1.save()

    # Retrieve user1 again to verify the update
    retrieved_user1 = User.get_by_discord_id(123456789, db_manager)
    print(retrieved_user1.timezone)  # Output: CST

    # Delete user2
    user2.delete()

    # Attempt to retrieve user2 (should be None)
    retrieved_user2 = User.get_by_discord_id(987654321, db_manager)
    print(retrieved_user2)  # Output: None

    db_manager.close()
    return


if __name__ == "__main__":
    main(sys.argv)
