import requests
import json

class RestStorage:
    def __init__(self, server_url="http://127.0.0.1:5000"):
        self.server_url = server_url.rstrip("/")
        self.api_prefix = self._detect_my_prefix()

    def _detect_my_prefix(self):
        try:
            response = requests.get(f"{self.server_url}/api/")
            response.raise_for_status()
            data = response.json()
            
            for num, title in data.get("sts", []):
                if "2501-04" in title or "0104" in title or "st04" in title.lower():
                    return f"/st{num}"
        except Exception as e:
            print(f"Не удалось определить префикс автоматически: {e}")
        
        return "/st4"

    def _url(self, path=""):
        return f"{self.server_url}{self.api_prefix}/api{path}"

    def get_all(self):
        r = requests.get(self._url("/employees"))
        r.raise_for_status()
        return r.json()

    def add(self, emp):
        data = {
            "type": emp.__class__.__name__,
            "data": {
                "name": emp.name,
                "age": emp.age,
                "department": getattr(emp, "department", ""),
                "title": getattr(emp, "title", "")
            }
        }
        r = requests.post(self._url("/employees"), json=data)
        r.raise_for_status()
        return r.json().get("id")

    def clear(self):
        r = requests.post(self._url("/employees/clear"))
        r.raise_for_status()