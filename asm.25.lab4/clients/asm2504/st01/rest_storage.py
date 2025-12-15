import requests

if __name__ == '__main__':
    from entity import Student, Starosta
else:
    from .entity import Student, Starosta

class Storage:
    def save_data(self, data):
        raise NotImplementedError
    def load_data(self):
        raise NotImplementedError

class RestStorage(Storage):
    def __init__(self, base_url="http://localhost:5000/st10/api/"):
        self.base_url = base_url if base_url.endswith('/') else base_url + '/'
        self.api_url = self.base_url
        self._timeout = 3

    def json_to_ent(self, data):
        ent_type = data.get('type')
        if ent_type == 'Starosta':
            ent = Starosta(None)
        else:
            ent = Student(None)

        ent.id = data.get('id')
        ignore = ['id', 'type']

        for k, v in data.items():
            if k not in ignore and hasattr(ent, k):
                setattr(ent, k, v)
        return ent

    def ent_to_dict(self, ent):
        data = {
            'type': ent.__class__.__name__,
            'name': ent.name,
            'age': ent.age
        }
        if hasattr(ent, 'group_role'):
            data['group_role'] = ent.group_role
        return data

    def get_entities(self):
        try:
            r = requests.get(self.api_url, timeout=self._timeout)
            r.raise_for_status()
            return [self.json_to_ent(i) for i in r.json()]
        except Exception as e:
            print(f"API Get Entities Error: {e}")
            return []

    def add_entity(self, item):
        data = self.ent_to_dict(item)
        try:
            r = requests.post(self.api_url, json=data, timeout=self._timeout)
            r.raise_for_status()
            # API should return created object (or at least its id)
            try:
                resp = r.json()
                item.id = resp.get('id', item.id)
            except Exception:
                # non-json response — ignore
                pass
            return True
        except Exception as e:
            print(f"API Add Error: {e}")
            return False

    def update_entity(self, item):
        if not item.id:
            return False
        data = self.ent_to_dict(item)
        try:
            r = requests.put(f"{self.api_url}{item.id}", json=data, timeout=self._timeout)
            r.raise_for_status()
            return True
        except Exception as e:
            print(f"API Update Error: {e}")
            return False

    def delete_entity(self, item_id):
        try:
            r = requests.delete(f"{self.api_url}{item_id}", timeout=self._timeout)
            r.raise_for_status()
            return True
        except Exception as e:
            print(f"API Delete Error: {e}")
            return False

    def delete_all_entities(self):
        try:
            r = requests.delete(self.api_url, timeout=self._timeout)
            r.raise_for_status()
            return True
        except Exception as e:
            print(f"API Delete All Error: {e}")
            return False

    def load_data(self):
        return self.get_entities()

    def save_data(self, data):
        if not data:
            print('There is nothing to save')
            return False

        ok_all = True
        # Replace remote data with provided list
        try:
            self.delete_all_entities()
        except Exception:
            # best-effort: continue to try adding
            pass

        for ent in data:
            ent.id = None
            ok = self.add_entity(ent)
            if not ok:
                ok_all = False
                print(f"Не удалось отправить запись: {ent}")

        if ok_all:
            print('Data was successfully saved to API')
        else:
            print('Some records failed to save to API')
        return ok_all

    # For compatibility with group.py
    def save(self, entities):
        self.save_data(entities)

    def load(self, entity_class_from_dict):
        # load_data returns fully reconstructed objects already
        entities = self.load_data()
        return entities