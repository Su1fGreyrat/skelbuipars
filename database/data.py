import sqlite3


class BotDB:
    def __init__(self, database_name='BotDB.db'):
        self.db = sqlite3.connect(database_name)
        self.cursor = self.db.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                name TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cities (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS key_words (
                id INTEGER PRIMARY KEY,
                word TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS selected (
                id INTEGER PRIMARY KEY,
                category_name TEXT,
                under_category_name TEXT,
                city TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY,
                name TEXT,
                link TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS under_categories (
                id INTEGER PRIMARY KEY,
                name TEXT,
                link TEXT
            )
        ''')
        
        self.db.commit()

    def new_user(self, user_id, name):
        user_exists = self.cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
        if not user_exists:
            self.cursor.execute('INSERT INTO users (user_id, name, balance, cart) VALUES (?, ?, 0, "")', (user_id, name))
        else:
            self.cursor.execute("UPDATE users SET name = ? WHERE user_id = ?", (name, user_id))
        self.db.commit()

    def get_users(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()
    
    def new_keyword(self, word):
        category_exists = self.cursor.execute("SELECT * FROM key_words WHERE word = ?", (word,)).fetchone()
        if not category_exists:
            self.cursor.execute("INSERT INTO key_words (word) VALUES (?)", (word,))
            self.db.commit()
            return f'Слово {word} добавленно'
        else:
            return f'Слово {word} уже существует'
            
    def get_keywords(self):
        words = self.cursor.execute("SELECT * FROM key_words").fetchall()
        return words
    
    def delete_keyword(self, word):
        category_exists = self.cursor.execute("SELECT * FROM key_words WHERE word = ?", (word,)).fetchone()
        
        if category_exists:
            self.cursor.execute("DELETE FROM key_words WHERE word = ?", (word,))
            self.db.commit()
            return f'Слово {word} удаленно'
        else:
            return f'Невозможно удалить слово {word}'
        
    def close_db(self):
        self.db.close()
