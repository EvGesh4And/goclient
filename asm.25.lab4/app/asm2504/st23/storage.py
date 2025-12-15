import sqlite3
import os
import pickle


class Storage:
    def __init__(self, db_path='data/asm2504/st23/menu.db'):
        os.makedirs('data/asm2504/st23', exist_ok=True)
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dishes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dish_type TEXT NOT NULL,
                    name TEXT NOT NULL,
                    cuisine TEXT NOT NULL,
                    calories INTEGER NOT NULL,
                    garnish TEXT,
                    sweetness INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    # ===== SQLite =====

    def add_item(self, item):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            dish_type = 'main' if hasattr(item, 'garnish') else 'dessert'

            cursor.execute('''
                INSERT INTO dishes (dish_type, name, cuisine, calories, garnish, sweetness)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                dish_type,
                item.name,
                item.cuisine,
                item.calories,
                getattr(item, 'garnish', None),
                getattr(item, 'sweetness', None)
            ))
            conn.commit()
            return True

    def get_items(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM dishes ORDER BY id')
            rows = cursor.fetchall()

            items = []
            for row in rows:
                item = self._row_to_dict(row)
                if item:
                    items.append(item)

            return items

    def get_item(self, index):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('SELECT id FROM dishes ORDER BY id')
            all_ids = cursor.fetchall()

            if not all_ids or index >= len(all_ids):
                return None

            real_id = all_ids[index][0]

            cursor.execute('SELECT * FROM dishes WHERE id = ?', (real_id,))
            row = cursor.fetchone()

            return self._row_to_dict(row) if row else None

    def update_item(self, index, item):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('SELECT id FROM dishes ORDER BY id')
            all_ids = cursor.fetchall()

            if not all_ids or index >= len(all_ids):
                return False

            real_id = all_ids[index][0]

            dish_type = 'main' if hasattr(item, 'garnish') else 'dessert'

            cursor.execute('''
                UPDATE dishes 
                SET dish_type = ?, name = ?, cuisine = ?, calories = ?, garnish = ?, sweetness = ?
                WHERE id = ?
            ''', (
                dish_type,
                item.name,
                item.cuisine,
                item.calories,
                getattr(item, 'garnish', None),
                getattr(item, 'sweetness', None),
                real_id
            ))
            conn.commit()
            return cursor.rowcount > 0

    def delete_item(self, index):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('SELECT id, name FROM dishes ORDER BY id')
            all_dishes = cursor.fetchall()

            if not all_dishes:
                return False

            if 0 <= index < len(all_dishes):
                real_id = all_dishes[index][0]

                cursor.execute('DELETE FROM dishes WHERE id = ?', (real_id,))
                conn.commit()
                return cursor.rowcount > 0
            else:
                return False

    def clear(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM dishes')
            conn.commit()

    # ===== PICKLE =====

    def save_to_pickle(self, filename):
        if not filename.endswith('.pkl'):
            filename += '.pkl'

        file_path = os.path.join('data/asm2504/st23', filename)

        try:
            dishes = self.get_items()
            with open(file_path, 'wb') as f:
                pickle.dump(dishes, f)
            return True
        except Exception as e:
            print(f"Ошибка при сохранении в pickle: {e}")
            return False

    def load_from_pickle(self, filename):
        if not filename.endswith('.pkl'):
            filename += '.pkl'

        file_path = os.path.join('data/asm2504/st23', filename)

        if not os.path.exists(file_path):
            return False

        try:
            with open(file_path, 'rb') as f:
                dishes = pickle.load(f)

            self.clear()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                for dish in dishes:
                    cursor.execute('''
                        INSERT INTO dishes (dish_type, name, cuisine, calories, garnish, sweetness)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        dish['dish_type'],
                        dish['name'],
                        dish['cuisine'],
                        dish['calories'],
                        dish.get('garnish'),
                        dish.get('sweetness')
                    ))

                conn.commit()

            return True

        except Exception as e:
            print(f"Ошибка при загрузке из pickle: {e}")
            return False

    def get_available_pickle_files(self):
        directory = "data/asm2504/st23"
        if not os.path.exists(directory):
            return []

        pkl_files = []
        for file in os.listdir(directory):
            if file.endswith('.pkl'):
                pkl_files.append(file)
        return sorted(pkl_files)

    # ===== ВСПОМОГАТЕЛЬНОЕ =====

    def _row_to_dict(self, row):
        if not row:
            return None

        id, dish_type, name, cuisine, calories, garnish, sweetness, created_at = row

        dish_dict = {
            'id': id,
            'dish_type': dish_type,
            'name': name,
            'cuisine': cuisine,
            'calories': calories,
            'garnish': garnish,
            'sweetness': sweetness,
            'created_at': created_at
        }

        return dish_dict

    # ===== СОВМЕСТИМОСТЬ =====

    def save(self, filename=None):
        return True

    def load(self, filename=None):
        return True

    def get_available_files(self, directory="data/asm2504/st23"):
        return self.get_available_pickle_files()