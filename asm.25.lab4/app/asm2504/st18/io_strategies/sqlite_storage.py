import sqlite3
import os
import pickle
from .flask_storage import FlaskStorage

class SQLiteStorage(FlaskStorage):
    def __init__(self, filename="university.db"):
        db_path = os.path.join(os.path.dirname(__file__), '../../../../data','asm504','st18', filename)
        self.filename = db_path
        self.objects = []
        self.init_db()
        self.load()
    
    def init_db(self):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        
        conn = sqlite3.connect(self.filename)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS people (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                data BLOB NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    
    def add(self, obj):
        self.objects.append(obj)
        self._save_to_db()
    
    def get(self, idx):
        if 0 <= idx < len(self.objects):
            return self.objects[idx]
        return None
    
    def update(self, idx, obj):
        if 0 <= idx < len(self.objects):
            self.objects[idx] = obj
            self._save_to_db()
    
    def delete(self, idx):
        if 0 <= idx < len(self.objects):
            del self.objects[idx]
            self._save_to_db()
    
    def clear(self):
        self.objects = []
        self._save_to_db()
    
    def save(self):
        self._save_to_db()
    
    def load(self):
        try:
            conn = sqlite3.connect(self.filename)
            cursor = conn.cursor()
            cursor.execute('SELECT data FROM people ORDER BY id')
            rows = cursor.fetchall()
            
            self.objects = []
            for row in rows:
                obj = pickle.loads(row[0])
                self.objects.append(obj)
            
            conn.close()
        except Exception as e:
            print(f"Ошибка загрузки из БД: {e}")
            self.objects = []
    
    def _save_to_db(self):
        try:
            conn = sqlite3.connect(self.filename)
            conn.execute('DELETE FROM people')  
            
            for obj in self.objects:
                data = pickle.dumps(obj)
                conn.execute('INSERT INTO people (type, data) VALUES (?, ?)', 
                           (obj.__class__.__name__, data))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Ошибка сохранения в БД: {e}")
    
    def import_from_pickle(self, filename):
        try:
            with open(filename, "rb") as f:
                imported_objects = pickle.load(f)
            
            for obj in imported_objects:
                self.add(obj)
            
            return len(imported_objects)
        except Exception as e:
            print(f"Ошибка импорта: {e}")
            return 0
    
    def set_filename(self, filename):
        db_path = os.path.join(os.path.dirname(__file__), '../../../../data','asm2504','st18' ,filename)
        self.filename = db_path
        self.objects = []
        self.init_db()
        self.load()
    
    def get_filename(self):
        return os.path.basename(self.filename)
    
    def get_available_files(self, folder="."):
        pkl_files = []
        
        if os.path.exists(folder):
            pkl_files = [f for f in os.listdir(folder) if f.endswith(".pkl")]
        
        return pkl_files