import sqlite3
import time

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
            CREATE TABLE IF NOT EXISTS admins (
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
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY,
                name TEXT,
                chat_id TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS adv (
                id INTEGER PRIMARY KEY,
                name TEXT,
                city TEXT,
                link TEXT
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
            self.cursor.execute('INSERT INTO users (user_id, name) VALUES (?, ?)', (user_id, name))
            self.db.commit()
        else:
            self.cursor.execute("UPDATE users SET name = ? WHERE user_id = ?", (name, user_id))
            self.db.commit()
            return 'user_ex'
            

    def get_users(self):
        users = self.cursor.execute('SELECT * FROM admins').fetchall()
        return users
    
    def new_keyword(self, word, category, under_category, city):
        category_exists = self.cursor.execute("SELECT * FROM key_words WHERE word = ? AND category = ? AND under_category = ? AND city = ?", (word, category, under_category, city)).fetchone()
        if not category_exists:
            self.cursor.execute("INSERT INTO key_words (word, category, under_category, city) VALUES (?,?,?,?)", (word, category, under_category, city))
            self.db.commit()
            return f'Запрос добавлен!\n\nСлово {word}\nКатегория: {category}\nПод категория: {under_category}\nГород: {city}'
        else:
            return f'Запрос со словом {word} с такими параметрами уже существует'
            
    def get_keywords(self):
        words = self.cursor.execute("SELECT * FROM key_words").fetchall()
        return words
    
    def delete_keyword(self, word, category, under_category, city):
        category_exists = self.cursor.execute("SELECT * FROM key_words WHERE word = ? AND category = ? AND under_category = ? AND city = ?", (word, category, under_category, city)).fetchone()
        
        if category_exists:
            self.cursor.execute("DELETE FROM key_words WHERE word = ?AND category = ? AND under_category = ? AND city = ?", (word, category, under_category, city))
            self.db.commit()
            return f'Слово {word} удалено\nКатегория: {category}\nПод категория: {under_category}\nГород: {city}\n'
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
    
    def get_link(self, category, under_category, city, kw):
        if under_category:
            city_id = self.cursor.execute("SELECT uniq_id FROM cities WHERE name = ?", (city, )).fetchone()
            u_link = self.cursor.execute("SELECT link FROM under_categories WHERE name = ?", (under_category, )).fetchone()
            keyword = kw.replace(' ', '+')
            print('wtf',keyword)
            link = str(u_link[0]) + f'?cities={city_id[0]}&keywords={keyword}'
            print(link)
        else:
            city_id = self.cursor.execute("SELECT uniq_id FROM cities WHERE name = ?", (city, )).fetchone()
            u_link = self.cursor.execute("SELECT link FROM categories WHERE name = ?", (category, )).fetchone()
            link = u_link + f'?cities={city_id}'
            
        return link
    
    def add_adv(self, name, city, link):
        adv_exsists = self.cursor.execute("SELECT * FROM adv WHERE name = ? AND link = ?", (name, link)).fetchall()
            
        if not adv_exsists:
            self.cursor.execute('INSERT INTO adv (name, city, link) VALUES (?,?,?)', (name, city, link))
            self.db.commit()
            return 'not_exists'
    
    def get_selectors_with_category(self, category):
        selectors = self.cursor.execute("SELECT * FROM selectors WHERE category_name = ?", (category, )).fetchall()
        return selectors
    
    def delete_selector(self, category, under_category, city):
        selector_exsits = self.cursor.execute("SELECT * FROM selectors WHERE category = ? AND under_category = ? AND city = ?", (category, under_category, city)).fetchone()
        if selector_exsits:
            self.cursor.execute("DELETE FROM selectors WHERE category = ? AND under_category = ? AND city = ?", (category, under_category, city))
            self.db.commit()
    
    def user_ex(self, user_id):
        user_ex = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id, )).fetchone()
        return user_ex
    
    def admin_ex(self, user_id):
        user_ex = self.cursor.execute("SELECT * FROM admins WHERE user_id = ?", (user_id, )).fetchone()
        if user_ex:
            return 0
        else:
            return None
    
    def add_chat(self, chat_id):
        chat_ex = self.cursor.execute("SELECT * FROM chats WHERE chat_id = ?", (chat_id,)).fetchone()
        if not chat_ex:
            self.cursor.execute("INSERT INTO chats (chat_id) VALUES (?)", (chat_id,))
            self.db.commit()
            return f'Чат добавлен'
        else:
            return f'Чат уже существует'
        
    def add_to_admins(self, user_id, name):
        admin_exists = self.cursor.execute('SELECT * FROM admins WHERE user_id = ?', (user_id,)).fetchone()
        if not admin_exists:
            self.cursor.execute('INSERT INTO admins (user_id, name) VALUES (?, ?)', (user_id, name))
            self.db.commit()
        else:
            self.cursor.execute("UPDATE admins SET name = ? WHERE user_id = ?", (name, user_id))
            self.db.commit()
            return 'admin_ex'
        
    def get_kw(self, category, under_category, city):
        kw = self.cursor.execute("SELECT * FROM key_words WHERE category = ? AND under_category = ? AND city = ?", (category, under_category, city)).fetchall()
        return kw   
        
    def get_chats(self):
        chats= self.cursor.execute("SELECT * FROM chats").fetchall()
        return chats     
    
    def get_requests(self, id):
        req = self.cursor.execute("SELECT * FROM key_words WHERE id = ?", (id,)).fetchone()
        return req     
    
    def delete_request(self, word, category, under_category, city):
        exists = self.cursor.execute("SELECT * FROM key_words WHERE word = ? AND category = ? AND under_category = ? AND city = ?", (word, category, under_category, city)).fetchone()
        
        if exists:
            self.cursor.execute("DELETE FROM key_words WHERE word = ? AND category = ? AND under_category = ? AND city = ?", (word, category, under_category, city))
            self.db.commit()
            answer = f'Слово {word} удалено\nКатегория: {category}\nПод категория: {under_category}\nГород: {city}\n'
        else:
            answer = f'Невозможно удалить слово {word}'
        
        selectors = self.cursor.execute("SELECT * FROM selectors").fetchall()
        if selectors:    
            for selector in selectors:
                kws = self.cursor.execute("SELECT * FROM key_words WHERE category = ? AND under_category = ? AND city = ?", (selector[1], selector[2], selector[3])).fetchall()
                if not kws:
                    self.cursor.execute("DELETE FROM selectors WHERE category_name = ? AND under_category_name = ? AND city = ?", (selector[1], selector[2], selector[3])).fetchall()
                    self.db.commit()
                
        return answer
        
          
    def close_db(self):
        self.db.close()
