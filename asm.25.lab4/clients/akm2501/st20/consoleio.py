class ConsoleIO:
    def input_data(self, prompt=""):
        return input(prompt)
    
    def output_data(self, data, field_name=""):
        print(f"{field_name}: {data}")
    
    def display_message(self, message):
        print(message)
    
    def display_error(self, error):
        print(f"Ошибка: {error}")