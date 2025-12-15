# В начале файла добавьте:
import sys
import os

# Добавляем текущую директорию в путь
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Затем импорты:
try:
    from .entities import Stock, Bond
except ImportError:
    from entities import Stock, Bond


class RESTStorage:
    """Стратегия хранения через REST API"""

    def __init__(self, base_url='http://127.0.0.1:5000/st29/api'):
        self.base_url = base_url

    def _make_request(self, method, endpoint, data=None):
        """Выполнить HTTP запрос"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, headers=headers, data=json.dumps(data))
            elif method == 'PUT':
                response = requests.put(url, headers=headers, data=json.dumps(data))
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)

            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"Ошибка API: {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Ошибка соединения: {e}")
            return None

    def save(self, data, filename=None):
        """Сохранить данные (не используется в REST)"""
        print("Сохранение через REST API не поддерживается")
        return False

    def load(self, filename=None):
        """Загрузить данные"""
        result = self._make_request('GET', 'assets')
        if result:
            # Нужно преобразовать JSON обратно в объекты
            from .entities import Stock, Bond
            instruments = []

            for item in result:
                if item['type'] == 'Акция':
                    instrument = Stock()
                    instrument.name = item['name']
                    instrument.price = item['price']
                    instrument.currency = item['currency']
                    instrument.dividend_yield = item.get('dividend_yield', 0.0)
                elif item['type'] == 'Облигация':
                    instrument = Bond()
                    instrument.name = item['name']
                    instrument.price = item['price']
                    instrument.currency = item['currency']
                    instrument.coupon_rate = item.get('coupon_rate', 0.0)
                    instrument.maturity_years = item.get('maturity_years', 1)
                    instrument.face_value = item.get('face_value', 1000.0)

                instruments.append(instrument)

            return instruments
        return []

    def add_instrument(self, instrument):
        """Добавить инструмент через API"""
        data = {
            'type': 'Акция' if hasattr(instrument, 'dividend_yield') else 'Облигация',
            'name': instrument.name,
            'price': instrument.price,
            'currency': instrument.currency
        }

        if hasattr(instrument, 'dividend_yield'):
            data['dividend_yield'] = instrument.dividend_yield
        else:
            data['coupon_rate'] = instrument.coupon_rate
            data['maturity_years'] = instrument.maturity_years
            data['face_value'] = instrument.face_value

        return self._make_request('POST', 'assets', data)

    def get_all_instruments(self):
        """Получить все инструменты"""
        return self.load()

    def get_instrument_count(self):
        """Получить количество инструментов"""
        result = self._make_request('GET', 'assets/count')
        return result.get('count', 0) if result else 0

    def get_total_value(self):
        """Получить общую стоимость"""
        result = self._make_request('GET', 'assets/total')
        return result.get('total_value', 0) if result else 0