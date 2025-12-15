import pickle
import os
import sqlite3
from abc import ABC, abstractmethod

class BaseStorage(ABC):
    @abstractmethod
    def get_all_items(self):
        pass
    
    @abstractmethod
    def get_item(self, item_id):
        pass
    
    @abstractmethod
    def add_item(self, item_data):
        pass
    
    @abstractmethod
    def update_item(self, item_id, item_data):
        pass
    
    @abstractmethod
    def delete_item(self, item_id):
        pass
    
    @abstractmethod
    def clear_all(self):
        pass
    
    @abstractmethod
    def save_to_file(self):
        pass
    
    @abstractmethod
    def load_from_file(self):
        pass

class PickleStorage(BaseStorage):
    def __init__(self, filename):
        self.filename = filename
        self.items_data = []
        self.max_id = 0
    
    def load_from_file(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'rb') as file:
                    data = pickle.load(file)
                    self.items_data = data.get('items_data', [])
                    self.max_id = data.get('max_id', 0)
                return True, f"Загружено {len(self.items_data)} записей из Pickle"
            return False, "Файл Pickle не существует"
        except Exception as e:
            return False, f"Ошибка загрузки из Pickle: {e}"
    
    def save_to_file(self):
        try:
            data = {'items_data': self.items_data, 'max_id': self.max_id}
            with open(self.filename, 'wb') as file:
                pickle.dump(data, file)
            return True, f"Сохранено {len(self.items_data)} записей в Pickle"
        except Exception as e:
            return False, f"Ошибка сохранения в Pickle: {e}"
    
    def get_all_items(self):
        from .person import Guest, Coach
        items = []
        for item_data in self.items_data:
            if item_data['type'] == 'Guest':
                item = Guest.from_dict(item_data)
            elif item_data['type'] == 'Coach':
                item = Coach.from_dict(item_data)
            else:
                continue
            items.append(item)
        return items
    
    def get_item(self, item_id):
        for item_data in self.items_data:
            if item_data.get('id') == item_id:
                from .person import Guest, Coach
                if item_data['type'] == 'Guest':
                    return Guest.from_dict(item_data)
                elif item_data['type'] == 'Coach':
                    return Coach.from_dict(item_data)
        return None
    
    def add_item(self, item_data):
        try:
            item_data['id'] = self.max_id
            self.items_data.append(item_data)
            self.max_id += 1
            return True
        except Exception as e:
            print(f"DEBUG: Exception in add_item: {e}")
            return False
    
    def update_item(self, item_id, item_data):
        for i, existing_data in enumerate(self.items_data):
            if existing_data.get('id') == item_id:
                for key, value in item_data.items():
                    self.items_data[i][key] = value
                return True
        return False
    
    def delete_item(self, item_id):
        for i, item_data in enumerate(self.items_data):
            if item_data.get('id') == item_id:
                del self.items_data[i]
                return True
        return False
    
    def clear_all(self):
        self.items_data = []
        self.max_id = 0
        return True

class SQLiteStorage(BaseStorage):
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                pass_type TEXT,
                training_type TEXT
            )
        """)
        conn.commit()
        conn.close()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def get_all_items(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items ORDER BY id")
        rows = cursor.fetchall()
        
        items = []
        for row in rows:
            item = {
                'id': row[0],
                'type': row[1],
                'name': row[2],
                'age': row[3],
                'pass_type': row[4] or '',
                'training_type': row[5] or ''
            }
            items.append(item)
        conn.close()
        return items
    
    def get_item(self, item_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        item = {
            'id': row[0],
            'type': row[1],
            'name': row[2],
            'age': row[3],
            'pass_type': row[4] or '',
            'training_type': row[5] or ''
        }
        conn.close()
        return item
    
    def add_item(self, item_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO items (type, name, age, pass_type, training_type)
                VALUES (?, ?, ?, ?, ?)
            """, (
                item_data.get('type', 'Guest'),
                item_data.get('name', ''),
                item_data.get('age', 0),
                item_data.get('pass_type', ''),
                item_data.get('training_type', '')
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка добавления в SQLite: {e}")
            return False
        finally:
            conn.close()
    
    def update_item(self, item_id, item_data):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT type FROM items WHERE id = ?", (item_id,))
            current_type = cursor.fetchone()[0]
            
            updates = []
            values = []
            
            if 'name' in item_data:
                updates.append("name = ?")
                values.append(item_data['name'])
            
            if 'age' in item_data:
                updates.append("age = ?")
                values.append(item_data['age'])
            
            if 'pass_type' in item_data and current_type == 'Guest':
                updates.append("pass_type = ?")
                values.append(item_data['pass_type'])
            
            if 'training_type' in item_data and current_type == 'Coach':
                updates.append("training_type = ?")
                values.append(item_data['training_type'])
            
            values.append(item_id)
            
            if updates:
                sql = f"UPDATE items SET {', '.join(updates)} WHERE id = ?"
                cursor.execute(sql, values)
                conn.commit()
            
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Ошибка обновления в SQLite: {e}")
            return False
        finally:
            conn.close()
    
    def delete_item(self, item_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            return False
        finally:
            conn.close()
    
    def clear_all(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM items")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='items'")
            conn.commit()
            return True
        except Exception as e:
            return False
        finally:
            conn.close()
    
    def save_to_file(self):
        return True, "Данные SQLite сохраняются автоматически"
    
    def load_from_file(self):
        return True, "Данные SQLite загружаются автоматически"