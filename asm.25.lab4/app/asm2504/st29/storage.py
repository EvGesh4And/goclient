import sqlite3
import pickle
import os


class SQLiteStorage:
    def __init__(self, db_path="data/asm2504/st29/assets.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            currency TEXT NOT NULL,
            dividend_yield REAL,
            coupon_rate REAL,
            maturity_years INTEGER,
            face_value REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        conn.commit()
        conn.close()

    def _asset_to_dict(self, asset):
        asset_dict = {
            'type': asset.get_type(),
            'name': asset.name,
            'price': asset.price,
            'currency': asset.currency,
            'dividend_yield': None,
            'coupon_rate': None,
            'maturity_years': None,
            'face_value': None
        }

        asset_type = asset.get_type()
        if asset_type == "Акция":
            asset_dict['dividend_yield'] = getattr(asset, 'dividend_yield', 0.0)
        elif asset_type == "Облигация":
            asset_dict['coupon_rate'] = getattr(asset, 'coupon_rate', 0.0)
            asset_dict['maturity_years'] = getattr(asset, 'maturity_years', 1)
            asset_dict['face_value'] = getattr(asset, 'face_value', 1000.0)

        return asset_dict

    def _dict_to_asset(self, data):
        asset_type = data['type']

        if asset_type == "Акция":
            from .stock import Stock
            asset = Stock(data.get('dividend_yield', 0.0))
        elif asset_type == "Облигация":
            from .bond import Bond
            asset = Bond(
                data.get('coupon_rate', 0.0),
                data.get('maturity_years', 1),
                data.get('face_value', 1000.0)
            )
        else:
            return None

        asset.name = data['name']
        asset.price = data['price']
        asset.currency = data['currency']
        asset.id = data['id']

        return asset

    def add_asset(self, asset):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        asset_dict = self._asset_to_dict(asset)

        cursor.execute('''
        INSERT INTO assets (type, name, price, currency, dividend_yield, coupon_rate, maturity_years, face_value)
        VALUES (:type, :name, :price, :currency, :dividend_yield, :coupon_rate, :maturity_years, :face_value)
        ''', asset_dict)

        conn.commit()
        conn.close()
        return True

    def edit_asset(self, index, asset):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM assets ORDER BY id LIMIT 1 OFFSET ?', (index,))
        result = cursor.fetchone()

        if not result:
            conn.close()
            return False

        asset_id = result[0]
        asset_dict = self._asset_to_dict(asset)
        asset_dict['id'] = asset_id

        cursor.execute('''
        UPDATE assets
        SET name = :name, price = :price, currency = :currency,
            dividend_yield = :dividend_yield, coupon_rate = :coupon_rate,
            maturity_years = :maturity_years, face_value = :face_value
        WHERE id = :id
        ''', asset_dict)

        conn.commit()
        conn.close()
        return True

    def delete_asset(self, index):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM assets ORDER BY id LIMIT 1 OFFSET ?', (index,))
        result = cursor.fetchone()

        if not result:
            conn.close()
            return False

        asset_id = result[0]
        cursor.execute('DELETE FROM assets WHERE id = ?', (asset_id,))  # ПРАВИЛЬНО: asset_id

        conn.commit()
        conn.close()
        return True

    def get_all_assets(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
        SELECT id, type, name, price, currency, dividend_yield, coupon_rate, maturity_years, face_value
        FROM assets
        ORDER BY id
        ''')

        assets = []
        for row in cursor.fetchall():
            data = {
                'id': row[0],
                'type': row[1],
                'name': row[2],
                'price': row[3],
                'currency': row[4],
                'dividend_yield': row[5],
                'coupon_rate': row[6],
                'maturity_years': row[7],
                'face_value': row[8]
            }
            asset = self._dict_to_asset(data)
            if asset:
                assets.append(asset)

        conn.close()
        return assets

    def get_asset(self, index):
        assets = self.get_all_assets()
        if 0 <= index < len(assets):
            return assets[index]
        return None

    def clear_all(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM assets')

        conn.commit()
        conn.close()
        return True

    def import_from_pickle(self, pickle_file="data/asm2504/st29/assets.dat"):
        if not os.path.exists(pickle_file):
            print(f"Файл {pickle_file} не существует")
            return False

        try:
            with open(pickle_file, 'rb') as file:
                pickle_assets = pickle.load(file)

            print(f"Загружено {len(pickle_assets)} активов из pickle")

            for asset in pickle_assets:
                self.add_asset(asset)

            print(f"Успешно импортировано {len(pickle_assets)} активов в БД")
            return True
        except Exception as e:
            print(f"Ошибка импорта из pickle: {e}")
            return False

    def export_to_pickle(self, pickle_file="data/asm2504/st29/assets.dat"):
        try:
            os.makedirs(os.path.dirname(pickle_file), exist_ok=True)

            assets = self.get_all_assets()
            with open(pickle_file, 'wb') as file:
                pickle.dump(assets, file)

            print(f"Успешно экспортировано {len(assets)} активов в {pickle_file}")
            return True
        except Exception as e:
            print(f"Ошибка экспорта в pickle: {e}")
            return False

    def get_asset_by_id(self, asset_id):
        """Получить актив по ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
        SELECT id, type, name, price, currency, dividend_yield, coupon_rate, maturity_years, face_value
        FROM assets WHERE id = ?
        ''', (asset_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            data = {
                'id': row[0],
                'type': row[1],
                'name': row[2],
                'price': row[3],
                'currency': row[4],
                'dividend_yield': row[5],
                'coupon_rate': row[6],
                'maturity_years': row[7],
                'face_value': row[8]
            }
            return self._dict_to_asset(data)
        return None