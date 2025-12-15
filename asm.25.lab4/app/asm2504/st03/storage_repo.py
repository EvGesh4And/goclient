import sqlite3
import os
import pickle

class SQLiteStorage:
    def __init__(self, db_path="data/asm2504/st03/menu.db", table_name="dishes"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.table_name = table_name
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dish_type TEXT NOT NULL,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                calories INTEGER NOT NULL,
                ingredients TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add(self, entity):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        entity_dict = entity.to_dict()
        
        columns = ', '.join(entity_dict.keys())
        placeholders = ':' + ', :'.join(entity_dict.keys())
        
        cursor.execute(f'''
            INSERT INTO {self.table_name} ({columns})
            VALUES ({placeholders})
        ''', entity_dict)
        
        conn.commit()
        conn.close()
        return True
    
    def update(self, id, entity):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        entity_dict = entity.to_dict()
        entity_dict['id'] = id
        
        set_clause = ', '.join([f"{key} = :{key}" for key in entity_dict.keys() if key != 'id'])
        
        cursor.execute(f'''
            UPDATE {self.table_name} 
            SET {set_clause}
            WHERE id = :id
        ''', entity_dict)
        
        conn.commit()
        conn.close()
        return True
    
    def delete(self, id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(f'DELETE FROM {self.table_name} WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return True
    
    def get_all(self, entity_factory):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(f'''
            SELECT * FROM {self.table_name} ORDER BY id
        ''')
        
        entities = []
        for row in cursor.fetchall():
            entity = entity_factory.from_row(row)
            entities.append(entity)
        
        conn.close()
        return entities
    
    def get_by_id(self, id, entity_factory):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(f'SELECT * FROM {self.table_name} WHERE id = ?', (id,))
        
        row = cursor.fetchone()
        if row:
            entity = entity_factory.from_row(row)
            conn.close()
            return entity
        
        conn.close()
        return None
    
    def clear_all(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(f'DELETE FROM {self.table_name}')
        conn.commit()
        conn.close()
        return True
    
    def import_data(self, data):
        try:
            self.clear_all()
            for entity in data:
                self.add(entity)
            return True
        except Exception as e:
            print(f"Ошибка импорта: {e}")
            return False
    
    def export_data(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(f'SELECT * FROM {self.table_name}')
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def save_to_file(self, data, filename="data/asm2504/st03/menu.dat"):
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'wb') as file:
                pickle.dump(data, file)
            return True
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            return False
    
    def load_from_file(self, filename="data/asm2504/st03/menu.dat"):
        try:
            with open(filename, 'rb') as file:
                return pickle.load(file)
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            return None