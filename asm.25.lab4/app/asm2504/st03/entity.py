class Dish:
    def __init__(self, dish_type="", name="", price=0.0, calories=0, ingredients=None):
        self.dish_type = dish_type
        self.name = name
        self.price = price
        self.calories = calories
        self.ingredients = ingredients or []
        self.id = None
    
    def get_type(self):
        return self.dish_type
    
    def input(self, io_handler):
        self.dish_type = io_handler.input_string('type')  
        self.name = io_handler.input_string('name')
        self.price = io_handler.input_float('price')
        self.calories = io_handler.input_number('calories')
        ingredients_str = io_handler.input_string('ingredients')
        self.ingredients = [i.strip() for i in ingredients_str.split(',') if i.strip()]
    
    def output(self, io_handler):
        io_handler.output('type', self.dish_type) 
        io_handler.output('name', self.name)
        io_handler.output('price', self.price)
        io_handler.output('calories', self.calories)
        io_handler.output('ingredients', ', '.join(self.ingredients))
    
    def to_dict(self):
        """Преобразует объект в словарь для сохранения в БД"""
        return {
            'dish_type': self.dish_type,
            'name': self.name,
            'price': self.price,
            'calories': self.calories,
            'ingredients': ','.join(self.ingredients) if self.ingredients else ''
        }
    
    @classmethod
    def from_dict(cls, data):
        """Создает объект из словаря"""
        dish = cls(
            dish_type=data['dish_type'],
            name=data['name'],
            price=data['price'],
            calories=data['calories'],
            ingredients=data['ingredients'].split(',') if data['ingredients'] else []
        )
        if 'id' in data:
            dish.id = data['id']
        return dish
    
    @classmethod
    def from_row(cls, row):
        """Создает объект Dish из row базы данных"""
        return cls.from_dict({
            'id': row[0],
            'dish_type': row[1],
            'name': row[2],
            'price': row[3],
            'calories': row[4],
            'ingredients': row[5]
        })