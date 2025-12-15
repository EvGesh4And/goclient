import requests

class RestStorage:

    def __init__(self, server_url="http://127.0.0.1:5000"):
        self.server_url = server_url.rstrip("/")
        self.api_prefix = self._detect_prefix()
        self.base_url = f"{self.server_url}{self.api_prefix}"
        print(f"Подключено к API: {self.base_url}")

    def _detect_prefix(self):
        try:
            response = requests.get(f"{self.server_url}/api/", timeout=3)
            data = response.json()

            for num, title in data.get("sts", []):
                if "st23" in title.lower() or "23" in title:
                    return f"/st{num}"

            return "/st23"
        except:
            return "/st23"

    def _url(self, path=""):
        return f"{self.base_url}/api{path}"

    def add_dish(self, dish_data):
        try:
            response = requests.post(self._url("/dishes"), json=dish_data, timeout=5)
            return response.status_code in [200, 201]
        except:
            return False

    def edit_dish(self, index, dish_data):
        try:
            response = requests.put(self._url(f"/dishes/{index}"), json=dish_data, timeout=5)
            return response.status_code == 200
        except:
            return False

    def delete_dish(self, index):
        try:
            response = requests.delete(self._url(f"/dishes/{index}"), timeout=5)
            return response.status_code == 200
        except:
            return False

    def clear_dishes(self):
        try:
            response = requests.delete(self._url("/dishes/clear"), timeout=5)
            return response.status_code == 200
        except:
            return False

    def get_all_dishes(self):
        try:
            response = requests.get(self._url("/dishes"), timeout=5)
            if response.status_code == 200:
                return response.json().get('dishes', [])
            return []
        except:
            return []

    def save_file(self, filename):
        try:
            response = requests.post(self._url("/save"), json={'filename': filename}, timeout=5)
            return response.status_code == 200
        except:
            return False

    def load_file(self, filename):
        try:
            response = requests.post(self._url("/load"), json={'filename': filename}, timeout=5)
            return response.status_code == 200
        except:
            return False

    def get_files(self):
        try:
            response = requests.get(self._url("/files"), timeout=5)
            if response.status_code == 200:
                return response.json().get('files', [])
            return []
        except:
            return []