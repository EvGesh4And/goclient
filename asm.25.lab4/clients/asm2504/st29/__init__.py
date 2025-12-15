# Создаем подмодуль main
import sys
import types

# Создаем модуль main
main_module = types.ModuleType('main')

# Импортируем функцию main из main.py
from .main import main as main_function

# Добавляем функцию main в модуль main
main_module.main = main_function

# Делаем main доступным как st29.main
sys.modules[__name__ + '.main'] = main_module

# Также экспортируем функцию main напрямую для других случаев
__all__ = ['main']