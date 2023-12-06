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
                name TEXT,
                uniq_id TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS key_words (
                id INTEGER PRIMARY KEY,
                word TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS selectors (
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
        
    def get_categories(self):
        categories = self.cursor.execute("SELECT * FROM categories").fetchall()
        return categories
    
    def get_under_categories(self, parametr):
        categories = self.cursor.execute("SELECT * FROM under_categories WHERE category = ?", (parametr,)).fetchall()
        return categories
        
    def get_cities(self):
        cities = self.cursor.execute("SELECT * FROM cities").fetchall()
        return cities
    
    def new_selector(self, category, under_category, city):
        selector_exsits = self.cursor.execute("SELECT * FROM selectors WHERE category_name = ? AND under_category_name = ? AND city = ?", (category, under_category, city)).fetchone()
        
        if not selector_exsits:
            self.cursor.execute("INSERT INTO selectors (category_name, under_category_name, city) VALUES (?,?,?)", (category, under_category, city))
            self.db.commit()
            return 0
        else:
            return 1
        
    def new_category(self, name, link):
        cat_exsists = self.cursor.execute("SELECT * FROM categories WHERE name = ?", (name,)).fetchone()
        
        if not cat_exsists:
            self.cursor.execute('INSERT INTO categories (name, link) VALUES (?,?)', (name, link))
            self.db.commit()
    
    def new_under_category(self, name, link, category):
        cat_exsists = self.cursor.execute("SELECT * FROM under_categories WHERE name = ?", (name,)).fetchone()
        
        if not cat_exsists:
            self.cursor.execute('INSERT INTO under_categories (name, link, category) VALUES (?,?,?)', (name, link, category))
            self.db.commit()
    def new_city(self, city, uniq_id):
        city_exsists = self.cursor.execute("SELECT * FROM cities WHERE name = ?", (city,)).fetchone()
        
        if not city_exsists:
            self.cursor.execute('INSERT INTO cities (name, uniq_id) VALUES (?,?)', (city, uniq_id))
            self.db.commit()
            
    def get_selectors(self):
        selectors = self.cursor.execute("SELECT * FROM selectors").fetchall()
        return selectors
    
    def get_link(self, category, under_category, city, page):
        if under_category:
            city_id = self.cursor.execute("SELECT uniq_id FROM cities WHERE name = ?", (city, )).fetchone()
            u_link = self.cursor.execute("SELECT link FROM under_categories WHERE name = ?", (under_category, )).fetchone()
            link = str(u_link[0]) + f'{page}?cities={city_id[0]}'
        else:
            city_id = self.cursor.execute("SELECT uniq_id FROM cities WHERE name = ?", (city, )).fetchone()
            u_link = self.cursor.execute("SELECT link FROM categories WHERE name = ?", (category, )).fetchone()
            link = u_link + f'{page}?cities={city_id}'
            
        return link
            
        
    def close_db(self):
        self.db.close()
