import requests
import pickle
from pathlib import Path

current = Path(__file__).resolve()
for parent in [current.parent] + list(current.parents):
    candidate = parent / "data" / "asm2504" / "st24"
    if candidate.exists():
        DATA_DIR = candidate
        break
else:
    DATA_DIR = current.parent / "data" / "asm2504" / "st24"
    DATA_DIR.mkdir(parents=True, exist_ok=True)


class RestStorage:
    def __init__(self, server_url="http://127.0.0.1:5000"):
        self.server_url = server_url.rstrip("/")
        self.DATA_DIR = DATA_DIR
        self.api_prefix = self._detect_prefix()

    def _detect_prefix(self):
        try:
            r = requests.get(f"{self.server_url}/api/")
            r.raise_for_status()
            for num, title in r.json().get("sts", []):
                if "2504-24" in title or "st24" in title.lower():
                    return f"/st{num}"
        except:
            pass
        return "/st9"

    def _url(self, path=""):
        return f"{self.server_url}{self.api_prefix}/api{path}"

    def get_all(self):
        r = requests.get(self._url("/employees"))
        r.raise_for_status()
        return r.json()

    def add(self, emp):
        payload = {
            "type": emp.__class__.__name__,
            "data": {
                "name": emp.name,
                "age": emp.age,
                "department": getattr(emp, "department", ""),
                "title": getattr(emp, "title", "")
            }
        }
        r = requests.post(self._url("/employees"), json=payload)
        r.raise_for_status()
        return r.json().get("id")

    def update(self, emp_id, emp):
        payload = {
            "data": {
                "name": emp.name,
                "age": emp.age,
                "department": getattr(emp, "department", ""),
                "title": getattr(emp, "title", "")
            }
        }
        r = requests.put(self._url(f"/employees/{emp_id}"), json=payload)
        r.raise_for_status()

    def clear(self):
        requests.post(self._url("/employees/clear")).raise_for_status()

    def save_to_file(self, filename="backup_client.pkl"):
        data = self.get_all()
        path = self.DATA_DIR / filename
        with open(path, "wb") as f:
            pickle.dump(data, f)
        print(f"Сохранено → {path}")

    def load_from_file(self, filename="backup_client.pkl"):
        path = self.DATA_DIR / filename
        if not path.exists():
            print(f"Файл не найден: {path}")
            return False

        try:
            with open(path, "rb") as f:
                employees = pickle.load(f)
            print(f"Загрузка {len(employees)} сотрудников из {path}...")
            self.clear()
            for item in employees:
                from .employee import Employee
                from .manager import Manager
                from .director import Director
                cls = {"Employee": Employee, "Manager": Manager, "Director": Director}.get(item["type"], Employee)
                emp = cls()
                emp.input_data_from_dict(item)
                self.add(emp)
            print("Данные загружены!")
            return True
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            return False

    def edit_by_id(self, emp_id):
        r = requests.get(self._url(f"/employees/{emp_id}"))
        if r.status_code == 404:
            print("Сотрудник не найден")
            return False
        r.raise_for_status()
        data = r.json()

        from .employee import Employee
        from .manager import Manager
        from .director import Director
        cls = {"Employee": Employee, "Manager": Manager, "Director": Director}.get(data["type"], Employee)
        emp = cls()
        emp.input_data_from_dict(data)

        print(f"\nРедактирование сотрудника:")
        print(f"   ID: {emp_id[:12]}...")
        print(f"   Тип: {data['type']}")
        print(f"   Имя: {data.get('name', '—')}")
        print(f"   Возраст: {data.get('age', '?')}")
        if data['type'] == 'Manager':
            print(f"   Департамент: {data.get('department', '—')}")
        if data['type'] == 'Director':
            print(f"   Должность: {data.get('title', '—')}")
        print("   ─" * 30)
        print("   Введите новые данные (Enter — оставить):")

        emp.input_data()
        self.update(emp_id, emp)
        print("Сотрудник успешно обновлён!")
        return True

    def search_by_name(self, name_part):
        try:
            all_emps = self.get_all()
            return [e for e in all_emps if name_part.lower() in e.get("name", "").lower()]
        except:
            return []