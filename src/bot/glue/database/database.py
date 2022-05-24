
import sqlite3 as sl
from typing import Optional


# add sqlite database class
class Database:
    def __init__(self, db):
        self.conn = sl.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)"
        )
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS principals (principal TEXT PRIMARY KEY, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES users(user_id))"
        )
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS canisters (canister_id TEXT PRIMARY KEY, standard TEXT, min INTEGER, max INTEGER, name TEXT)"
        )
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS checks (canister_id TEXT, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES users(user_id), FOREIGN KEY(canister_id) REFERENCES canisters(canister_id))"
        )
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS guilds (guild_id INTEGER PRIMARY KEY, tier TEXT)"
        )
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS verifies ( guild_id INTEGER, canister_id TEXT, FOREIGN KEY(guild_id) REFERENCES guilds(guild_id), FOREIGN KEY(canister_id) REFERENCES canisters(canister_id))"
        )
        self.conn.commit()

    # users

    def fetch_users(self):
        """Fetch all users from the database"""
        self.cur.execute("SELECT * FROM users")
        rows = self.cur.fetchall()
        return rows

    def insert_user(self, user_id: int):
        """Insert a user into the database"""
        self.cur.execute("INSERT INTO users VALUES (?)",
                         (user_id,))
        self.conn.commit()

    def remove_user(self, user_id: int):
        """Remove a user from the database"""
        self.cur.execute("DELETE FROM users WHERE user_id=?", (user_id,))
        self.conn.commit()

    # principals

    def fetch_principals(self):
        """Fetch all principals from the database"""
        self.cur.execute("SELECT * FROM principals")
        rows = self.cur.fetchall()
        return rows

    def insert_principal(self, principal: str, user_id: int):
        """Insert a principal into the database"""
        self.cur.execute("INSERT INTO principals VALUES (?, ?)",
                         (principal, user_id))
        self.conn.commit()

    def remove_principal(self, principal: str):
        """Remove a principal from the database"""
        self.cur.execute(
            "DELETE FROM principals WHERE principal=?", (principal,))
        self.conn.commit()

    # canisters

    def fetch_canisters(self):
        """Fetch all canisters from the database"""
        self.cur.execute("SELECT * FROM canisters")
        rows = self.cur.fetchall()
        return rows

    def insert_canister(self, canister_id: str, standard: str, min: int, max: Optional[int], name: str):
        """Insert a canister into the database"""
        self.cur.execute("INSERT INTO canisters VALUES (?, ?, ?, ?, ?)",
                         (canister_id, standard, min, max, name))
        self.conn.commit()

    def remove_canister(self, canister_id):
        """Remove a canister from the database"""
        self.cur.execute("DELETE FROM canisters WHERE canister_id=?",
                         (canister_id,))
        self.conn.commit()

    # checks

    def fetch_checks(self):
        """Fetch all checks from the database"""
        self.cur.execute("SELECT * FROM checks")
        rows = self.cur.fetchall()
        return rows

    def insert_check(self, canister_id: str, user_id: int):
        """Insert a check into the database"""
        self.cur.execute("INSERT INTO checks VALUES (?, ?)",
                         (canister_id, user_id))
        self.conn.commit()

    def remove_check(self, canister_id: str, user_id: int):
        self.cur.execute("DELETE FROM checks WHERE canister_id=? AND user_id=?",
                         (canister_id, user_id))
        self.conn.commit()

    # guilds

    def fetch_guilds(self):
        """Fetch all guilds from the database"""
        self.cur.execute("SELECT * FROM guilds")
        rows = self.cur.fetchall()
        return rows

    def insert_guild(self, guild_id: int, tier: str):
        """Insert a guild into the database"""
        self.cur.execute("INSERT INTO guilds VALUES (?, ?)",
                         (guild_id, tier))
        self.conn.commit()

    def remove_guild(self, guild_id: int):
        """Remove a guild from the database"""
        self.cur.execute("DELETE FROM guilds WHERE guild_id=?",
                         (guild_id,))
        self.conn.commit()

    # verifies

    def fetch_verifies(self):
        """Fetch all verifies from the database"""
        self.cur.execute("SELECT * FROM verifies")
        rows = self.cur.fetchall()
        return rows

    def insert_verify(self, guild_id: int, canister_id: str):
        """Insert a verify into the database"""
        self.cur.execute("INSERT INTO verifies VALUES (?, ?)",
                         (guild_id, canister_id))
        self.conn.commit()

    def remove_verify(self, guild_id: int, canister_id: str):
        """Remove a verify from the database"""
        self.cur.execute("DELETE FROM verifies WHERE guild_id=? AND canister_id=?",
                         (guild_id, canister_id))
        self.conn.commit()

    # called when reference to the object is destroyed, eg garbage collected
    def __del__(self):
        self.conn.close()
