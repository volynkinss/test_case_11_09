import sqlite3
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s"
)


class Chat_DB:
    users_table = "users"
    character_table = "character"
    dialog_table = "dialog"

    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        logging.info(f"Connected to SQLite database: {self.db_name}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            logging.info(f"Disconnected from SQLite database: {self.db_name}")

    def execute_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()
        logging.info("Query executed successfully")

    def create_table(self, table_name, coloumns):
        create_query = f"""CREATE TABLE IF NOT EXISTS {table_name} ({coloumns})"""
        self.execute_query(create_query)
        logging.info(f"Table '{table_name}' created successfully")

    def create_user(self, user_id, username, name, surname):
        insert_query = f"INSERT OR IGNORE INTO {self.users_table} (user_id, username, name, surname) VALUES {user_id, username, name, surname}"
        self.execute_query(insert_query)
        logging.info("Users Data inserted successfully")

    def selection_record(self, user_id, user_selection):
        insert_query = f"INSERT OR IGNORE INTO {self.character_table} (user_id, character) VALUES {user_id, user_selection}"
        self.execute_query(insert_query)
        logging.info("User selection data inserted successfully")

    def users_msg(self, user_id, message):
        insert_query = f"INSERT OR IGNORE INTO {self.dialog_table} (user_id, user_msg) VALUES {user_id, message}"
        self.execute_query(insert_query)
        logging.info("User msg data inserted successfully")

    def answer_msg(self, user_id, message):
        insert_query = f"""UPDATE {self.dialog_table} SET bot_answer_msg = "{message}" WHERE user_id = {user_id}"""
        self.execute_query(insert_query)
        logging.info("Bot answer msg data inserted successfully")

    def drop_table(self, table_name):
        query = f"DROP TABLE IF EXISTS {table_name}"
        self.cursor.execute(query)
        self.connection.commit()
        logging.info(f"Table {table_name} has been dropped successfully.")

    def init_chat_tables(self):
        self.drop_table(self.users_table)
        self.drop_table(self.character_table)
        self.drop_table(self.dialog_table)

        create_users_table = """
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username STRING,
            name STRING,
            surname STRING,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            """
        self.create_table(self.users_table, create_users_table)
        create_character_table = """
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            character STRING,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            """
        self.create_table(self.character_table, create_character_table)
        create_dialog_table = """
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_msg TEXT,
            bot_answer_msg TEXT
            """
        self.create_table(self.dialog_table, create_dialog_table)

    def fetch_data(self, query):
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            logging.info(f"Error fetching data: {e}")
            return []

    def fetch_all_data(self):
        rows = self.fetch_data(f"SELECT * FROM {self.users_table}")
        for row in rows:
            logging.info(row)
        rows = self.fetch_data(f"SELECT * FROM {self.character_table}")
        for row in rows:
            logging.info(row)
        rows = self.fetch_data(f"SELECT * FROM {self.dialog_table}")
        for row in rows:
            logging.info(row)
