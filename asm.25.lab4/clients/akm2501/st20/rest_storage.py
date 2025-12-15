import requests
from .models import MedicalItem
from typing import Optional, List, Dict, Any
import time

class RestStorage:
    def __init__(self, base_url: Optional[str] = None, max_retries: int = 3, retry_delay: int = 2):
        # Для папки st20 всегда используем st0120
        self.base_url = base_url or "http://localhost:5000/st0120/api"
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'MedicalCatalogClient/1.0'
        })
        
        print(f"Автоматическое подключение к: {self.base_url}")
    
    def _retry_request(self, method: str, endpoint: str, **kwargs):
        """Метод с повторными попытками подключения"""
        url = f'{self.base_url}/{endpoint}'.rstrip('/')
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.request(method, url, timeout=10, **kwargs)
                response.raise_for_status()
                return response
                
            except requests.exceptions.ConnectionError as e:
                if attempt < self.max_retries - 1:
                    print(f"Попытка {attempt + 1}/{self.max_retries} не удалась. Повтор через {self.retry_delay} сек...")
                    time.sleep(self.retry_delay)
                else:
                    print(f"Не удалось подключиться к серверу после {self.max_retries} попыток")
                    print(f"Убедитесь, что веб-сервер запущен: python lab4.py")
                    raise
            
            except requests.exceptions.Timeout:
                print(f"Таймаут подключения к {self.base_url}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    print("Превышено время ожидания сервера")
                    raise
            
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    print(f"Эндпоинт не найден: {url}")
                elif e.response.status_code == 401:
                    print("Ошибка авторизации. Проверьте учетные данные.")
                elif e.response.status_code == 500:
                    print("Ошибка сервера. Попробуйте позже.")
                raise
            
            except requests.exceptions.RequestException as e:
                print(f"Ошибка запроса: {e}")
                raise
        
        return None
    
    def check_connection(self) -> bool:
        """Проверка соединения с сервером"""
        print("Проверка соединения с сервером...")
        try:
            # Попробуем получить доступ к корневому эндпоинту или /items
            response = self.session.get(self.base_url.rstrip('/'), timeout=5)
            
            # Если сервер отвечает, даже с ошибкой 404 - это хорошо
            print("✓ Соединение установлено")
            return True
            
        except requests.exceptions.ConnectionError:
            print("✗ Не удалось подключиться к серверу")
            print(f"Убедитесь, что веб-сервер запущен на {self.base_url}")
            print("Команда для запуска: python lab4.py")
            return False
            
        except requests.exceptions.Timeout:
            print("✗ Таймаут при подключении к серверу")
            return False
            
        except Exception as e:
            print(f"✗ Ошибка при проверке соединения: {e}")
            return False
    
    def wait_for_server(self, timeout: int = 30) -> bool:
        """Ожидание запуска сервера"""
        print("Ожидание запуска сервера...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.check_connection():
                return True
            print("Сервер не отвечает. Повторная попытка через 3 секунды...")
            time.sleep(3)
        
        print(f"Сервер не запустился за {timeout} секунд")
        return False
    
    def get_all_items(self) -> List[MedicalItem]:
        """Получить все медицинские изделия"""
        try:
            response = self._retry_request('GET', 'items')
            items_data = response.json()
            
            items = []
            for item_data in items_data:
                try:
                    item = MedicalItem.from_dict(item_data)
                    items.append(item)
                except Exception as e:
                    print(f"Ошибка при преобразовании данных: {e}")
                    continue
            
            return items
            
        except Exception as e:
            print(f"Не удалось получить данные: {e}")
            return []
    
    def get_item(self, item_id: int) -> Optional[MedicalItem]:
        """Получить конкретное медицинское изделие по ID"""
        try:
            response = self._retry_request('GET', f'items/{item_id}')
            item_data = response.json()
            return MedicalItem.from_dict(item_data)
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"Запись с ID {item_id} не найдена")
            return None
            
        except Exception as e:
            print(f"Ошибка при получении записи: {e}")
            return None
    
    def add_item(self, item: MedicalItem) -> tuple[bool, str]:
        """Добавить новое медицинское изделие"""
        try:
            response = self._retry_request('POST', 'items', json=item.to_dict())
            
            if response.status_code == 201:
                print("✓ Запись успешно добавлена")
                return True, "Запись успешно добавлена"
            else:
                return False, f"Ошибка сервера: {response.status_code}"
                
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                error_msg = e.response.json().get('error', 'Неверные данные')
                return False, f"Ошибка валидации: {error_msg}"
            return False, f"HTTP ошибка: {e.response.status_code}"
            
        except Exception as e:
            print(f"Ошибка при добавлении записи: {e}")
            return False, f"Ошибка подключения: {str(e)}"
    
    def update_item(self, item: MedicalItem) -> tuple[bool, str]:
        """Обновить существующее медицинское изделие"""
        try:
            response = self._retry_request('PUT', f'items/{item.id}', json=item.to_dict())
            
            if response.status_code == 200:
                print("✓ Запись успешно обновлена")
                return True, "Запись успешно обновлена"
            else:
                return False, f"Ошибка сервера: {response.status_code}"
                
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return False, f"Запись с ID {item.id} не найдена"
            return False, f"HTTP ошибка: {e.response.status_code}"
            
        except Exception as e:
            print(f"Ошибка при обновлении записи: {e}")
            return False, f"Ошибка подключения: {str(e)}"
    
    def delete_item(self, item_id: int) -> tuple[bool, str]:
        """Удалить медицинское изделие"""
        try:
            response = self._retry_request('DELETE', f'items/{item_id}')
            
            if response.status_code == 200:
                print("✓ Запись успешно удалена")
                return True, "Запись успешно удалена"
            else:
                return False, f"Ошибка сервера: {response.status_code}"
                
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return False, f"Запись с ID {item_id} не найдена"
            return False, f"HTTP ошибка: {e.response.status_code}"
            
        except Exception as e:
            print(f"Ошибка при удалении записи: {e}")
            return False, f"Ошибка подключения: {str(e)}"
    
    def get_stats(self) -> Dict[str, Any]:
        """Получить статистику"""
        try:
            response = self._retry_request('GET', 'stats')
            return response.json()
            
        except Exception as e:
            print(f"Ошибка при получении статистики: {e}")
            return {}