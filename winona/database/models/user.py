#!/usr/bin/env python3

from typing import Optional
import sys


from typing import Optional

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
                 user_id: Optional[int] = None):
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
        """
        self.discord_name = discord_name
        self.discord_name_in_server = discord_name_in_server
        self.discord_id = discord_id
        self.pogo_trainer_name = pogo_trainer_name
        self.pogo_trainer_code = pogo_trainer_code
        self.timezone = timezone
        self.user_id = user_id
        return

    def __repr__(self):
        """
        Returns a string representation of the User object.
        """
        return f"<User discord_name='{self.discord_name}' discord_id='{self.discord_id}'>"

    def __str__(self):
        """
        Returns a user-friendly string representation of the User object.
        """
        return (f"User ID: {self.user_id if self.user_id is not None else 'N/A'}\n"
                f"Discord Name: {self.discord_name}\n"
                f"Server Nickname: {self.discord_name_in_server}\n"
                f"Discord ID: {self.discord_id}\n"
                f"PoGo Trainer Name: {self.pogo_trainer_name}\n"
                f"PoGo Trainer Code: {self.pogo_trainer_code}\n"
                f"Timezone: {self.timezone}")


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
