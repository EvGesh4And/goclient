import os
import sys
from urllib.parse import parse_qs
from jinja2 import Environment, FileSystemLoader

sys.path.append(os.path.dirname(__file__))

from pet_shop import PetShop
from io_strategy import WSGIIOStrategy
from storage import SQLiteStorage

class PetShopWSGI:
    def __init__(self):
        self.template_env = Environment(loader=FileSystemLoader('app/templates'))
        self.storage = SQLiteStorage()
    
    def parse_form_data(self, environ):
        """Парсинг данных формы из WSGI environ"""
        try:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            if content_length > 0:
                post_data = environ['wsgi.input'].read(content_length).decode('utf-8')
                return parse_qs(post_data)
            return {}
        except (ValueError, KeyError):
            return {}
    
    def get_path_segments(self, path):
        """Разбивает путь на сегменты"""
        return [segment for segment in path.split('/') if segment]
    
    def render_template(self, template_name, **context):
        """Рендерит шаблон Jinja2"""
        template = self.template_env.get_template(f"akm2501/st11/{template_name}")
        return template.render(**context).encode('utf-8')
   
    def redirect(self, location):
        """Создает redirect response"""
        return ('302 Found', [('Location', location)], [])
    
    def serve_static(self, environ, start_response):
        """Обслуживание статических файлов"""
        path = environ['PATH_INFO'][1:]  
        
        static_paths = [
            os.path.join('app', 'static', path),  
            os.path.join('static', path),         
            path                                 
        ]
        
        for static_path in static_paths:
            if os.path.exists(static_path) and os.path.isfile(static_path):
                try:
                    with open(static_path, 'rb') as f:
                        content = f.read()
                    
                    if path.endswith('.css'):
                        content_type = 'text/css'
                    elif path.endswith('.js'):
                        content_type = 'application/javascript'
                    elif path.endswith('.png'):
                        content_type = 'image/png'
                    elif path.endswith('.jpg') or path.endswith('.jpeg'):
                        content_type = 'image/jpeg'
                    else:
                        content_type = 'text/plain'
                    
                    start_response('200 OK', [('Content-Type', content_type)])
                    return [content]
                except Exception:
                    continue
        
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'Static file not found']
    
    def handle_show_animals(self, environ, start_response):
        """Показать всех животных"""
        shop = PetShop(WSGIIOStrategy(), self.storage)
        animals = shop.show_catalog()
        html = self.render_template('animals_list.html', animals=animals)
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        return [html]
    
    def handle_create_animal_form(self, environ, start_response):
        """Показать форму создания животного"""
        html = self.render_template('create_animal.html')
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        return [html]
    
    def handle_add_animal(self, environ, start_response):
        """Обработать добавление животного"""
        form_data = self.parse_form_data(environ)
        shop = PetShop(WSGIIOStrategy(form_data), self.storage)
        message = shop.add_animal()
       
        response_headers = [
            ('Location', '/show_animals'),
            ('Content-Type', 'text/html; charset=utf-8')
        ]
        start_response('302 Found', response_headers)
        return [f'<html><body><script>alert("{message}"); window.location="/show_animals";</script></body></html>'.encode('utf-8')]
    
    def handle_edit_animal_form(self, environ, start_response, animal_id):
        """Показать форму редактирования животного"""
        shop = PetShop(WSGIIOStrategy(), self.storage)
        animal = shop.get_by_id(animal_id)
        
        if not animal:
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return [b'Animal not found']
        
        html = self.render_template('edit_animal.html', animal=animal)
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        return [html]
    
    def handle_confirm_edit(self, environ, start_response, animal_id):
        """Обработать редактирование животного"""
        form_data = self.parse_form_data(environ)
        shop = PetShop(WSGIIOStrategy(form_data), self.storage)
        message = shop.edit_animal(animal_id)
        
        response_headers = [
            ('Location', '/show_animals'),
            ('Content-Type', 'text/html; charset=utf-8')
        ]
        start_response('302 Found', response_headers)
        return [f'<html><body><script>alert("{message}"); window.location="/show_animals";</script></body></html>'.encode('utf-8')]
    
    def handle_delete_animal(self, environ, start_response, animal_id):
        """Обработать удаление животного"""
        shop = PetShop(WSGIIOStrategy(), self.storage)
        message = shop.delete_animal(animal_id)
        
        response_headers = [
            ('Location', '/show_animals'),
            ('Content-Type', 'text/html; charset=utf-8')
        ]
        start_response('302 Found', response_headers)
        return [f'<html><body><script>alert("{message}"); window.location="/show_animals";</script></body></html>'.encode('utf-8')]
    
    def handle_index(self, environ, start_response):
        """Главная страница"""
        html = self.render_template('index.html')
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        return [html]
    
    def handle_dump(self, environ, start_response):
        """Сохранение данных"""
        shop = PetShop(WSGIIOStrategy(), self.storage)
        message = shop.save()
        
        response_headers = [
            ('Location', '/show_animals'),
            ('Content-Type', 'text/html; charset=utf-8')
        ]
        start_response('302 Found', response_headers)
        return [f'<html><body><script>alert("{message}"); window.location="/show_animals";</script></body></html>'.encode('utf-8')]
    
    def handle_load(self, environ, start_response):
        """Загрузка данных"""
        shop = PetShop(WSGIIOStrategy(), self.storage)
        message = shop.load()
        
        response_headers = [
            ('Location', '/show_animals'),
            ('Content-Type', 'text/html; charset=utf-8')
        ]
        start_response('302 Found', response_headers)
        return [f'<html><body><script>alert("{message}"); window.location="/show_animals";</script></body></html>'.encode('utf-8')]
    
    def handle_clear(self, environ, start_response):
        """Очистка каталога"""
        shop = PetShop(WSGIIOStrategy(), self.storage)
        message = shop.clear_catalog()
        
        response_headers = [
            ('Location', '/show_animals'),
            ('Content-Type', 'text/html; charset=utf-8')
        ]
        start_response('302 Found', response_headers)
        return [f'<html><body><script>alert("{message}"); window.location="/show_animals";</script></body></html>'.encode('utf-8')]
    
    def not_found(self, environ, start_response):
        """Обработка 404 ошибки"""
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'Page not found']
    
    def __call__(self, environ, start_response):
        method = environ['REQUEST_METHOD']
        path = environ['PATH_INFO']
        
        if path.startswith('/static/') or any(path.endswith(ext) for ext in ['.css', '.js', '.png', '.jpg', '.jpeg']):
            return self.serve_static(environ, start_response)
        
        segments = self.get_path_segments(path)
        
        try:
            if path == '/' and method == 'GET':
                return self.handle_index(environ, start_response)
            elif path == '/show_animals' and method == 'GET':
                return self.handle_show_animals(environ, start_response)
            elif path == '/create_animal' and method == 'GET':
                return self.handle_create_animal_form(environ, start_response)
            elif path == '/create_animal' and method == 'POST':
                return self.handle_add_animal(environ, start_response)
            elif len(segments) == 2 and segments[0] == 'edit_animal' and method == 'GET':
                return self.handle_edit_animal_form(environ, start_response, segments[1])
            elif len(segments) == 2 and segments[0] == 'edit_animal' and method == 'POST':
                return self.handle_confirm_edit(environ, start_response, segments[1])
            elif len(segments) == 2 and segments[0] == 'delete_animal' and method == 'GET':
                return self.handle_delete_animal(environ, start_response, segments[1])
            elif path == '/dump' and method == 'GET':
                return self.handle_dump(environ, start_response)
            elif path == '/load' and method == 'GET':
                return self.handle_load(environ, start_response)
            elif path == '/clear' and method == 'GET':
                return self.handle_clear(environ, start_response)
            else:
                return self.not_found(environ, start_response)
        except Exception as e:
            start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
            return [f'Server error: {str(e)}'.encode('utf-8')]

application = PetShopWSGI()

def create_app():
    return PetShopWSGI()
   
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    try:
        hosts = ['localhost']
        port = 8000
        
        for host in hosts:
            try:
                print(f"Пробую запустить на {host}:{port}...")
                server = make_server(host, port, application)
                print(f"Сервер запущен на http://{host}:{port}")
                break
            except Exception as e:
                print(f" Не удалось на {host}: {e}")
                continue
        else:
            print(" Не удалось запустить сервер ни на одном хосте")
            input("Нажмите Enter для выхода...")
            exit(1)
            
        print("Доступные routes:")
        print("  GET  / - главная страница")
        print("  GET  /show_animals - список животных")
        print("  GET  /create_animal - форма добавления")
        print("  POST /create_animal - добавление животного")
        print("  GET  /edit_animal/<id> - форма редактирования")
        print("  POST /edit_animal/<id> - сохранение изменений")
        print("  GET  /delete_animal/<id> - удаление животного")
        print("  GET  /dump - сохранение данных")
        print("  GET  /load - загрузка данных")
        print("  GET  /clear - очистка каталога")
        
        print("Сервер готов принимать подключения...")
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\nСервер остановлен")
    except Exception as e:
        print(f"Ошибка: {e}")
        input("Нажмите Enter для выхода...")