import sys
import os

# Добавляем путь к модулям
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from .console_io import ConsoleIO
    from .entities import Stock, Bond, FinancialInstrument
    from .api_client import RESTStorage
except ImportError:
    from console_io import ConsoleIO
    from entities import Stock, Bond, FinancialInstrument
    from api_client import RESTStorage


class RESTFinancialInstrument(FinancialInstrument):
    """Финансовый инструмент с поддержкой REST"""

    def __init__(self, name="", price=0.0, currency="USD", io_strategy=None):
        super().__init__(name, price, currency, io_strategy)
        self.rest_storage = RESTStorage()

    def save_to_cloud(self):
        """Сохранить инструмент через REST API"""
        return self.rest_storage.add_instrument(self)


class InvestmentPortfolioREST:
    """Портфель с REST API"""

    def __init__(self):
        self.rest_storage = RESTStorage()
        self.io_strategy = ConsoleIO()

    def display_all(self):
        """Вывести весь портфель"""
        instruments = self.rest_storage.get_all_instruments()

        if not instruments:
            self.io_strategy.output_message("Портфель пуст.")
            return

        self.io_strategy.output_message("\n" + "=" * 60)
        self.io_strategy.output_message(" ИНВЕСТИЦИОННЫЙ ПОРТФЕЛЬ (REST API)")
        self.io_strategy.output_message("=" * 60)

        total_value = 0
        for i, instrument in enumerate(instruments, 1):
            self.io_strategy.output_message(f"\n{i}.")
            instrument.output()
            total_value += instrument.price
            self.io_strategy.output_message("-" * 40)

        self.io_strategy.output_message(f"\nОбщая стоимость портфеля: {total_value:,.2f}")
        self.io_strategy.output_message("=" * 60)

    def add_instrument_menu(self):
        """Меню добавления инструмента"""
        self.io_strategy.output_message("\n--- ДОБАВЛЕНИЕ ФИНАНСОВОГО ИНСТРУМЕНТА ---")
        self.io_strategy.output_message("1. Акция")
        self.io_strategy.output_message("2. Облигация")

        try:
            instrument_type = self.io_strategy.input_number("Выберите тип инструмента")

            if instrument_type == 1:
                instrument = Stock()
            elif instrument_type == 2:
                instrument = Bond()
            else:
                self.io_strategy.output_error("Неверный тип инструмента")
                return

            instrument.input()

            # Сохраняем через REST API
            if self.rest_storage.add_instrument(instrument):
                self.io_strategy.output_message("Инструмент успешно добавлен через REST API!")
            else:
                self.io_strategy.output_error("Ошибка при добавлении инструмента")

        except Exception as e:
            self.io_strategy.output_error(f"Ошибка: {e}")

    def show_stats(self):
        """Показать статистику"""
        count = self.rest_storage.get_instrument_count()
        total_value = self.rest_storage.get_total_value()

        self.io_strategy.output_message("\n--- СТАТИСТИКА ПОРТФЕЛЯ ---")
        self.io_strategy.output_message(f"Количество инструментов: {count}")
        self.io_strategy.output_message(f"Общая стоимость: {total_value:,.2f}")

    def run(self):
        """Запуск консольного клиента"""
        while True:
            try:
                self.io_strategy.output_message("\n" + "=" * 50)
                self.io_strategy.output_message(" КОНСОЛЬНЫЙ КЛИЕНТ REST API")
                self.io_strategy.output_message("=" * 50)
                self.io_strategy.output_message("1. Добавить инструмент")
                self.io_strategy.output_message("2. Показать портфель")
                self.io_strategy.output_message("3. Статистика")
                self.io_strategy.output_message("0. Выход")
                self.io_strategy.output_message("=" * 50)

                choice = self.io_strategy.input_number("Выберите действие")

                if choice == 0:
                    self.io_strategy.output_message("Выход из программы.")
                    break
                elif choice == 1:
                    self.add_instrument_menu()
                elif choice == 2:
                    self.display_all()
                elif choice == 3:
                    self.show_stats()
                else:
                    self.io_strategy.output_error("Неверный выбор")

            except KeyboardInterrupt:
                self.io_strategy.output_message("\n\nПрограмма завершена.")
                break
            except Exception as e:
                self.io_strategy.output_error(f"Ошибка: {e}")


def main():
    """Основная функция"""
    try:
        print("Запуск консольного клиента REST API...")
        portfolio = InvestmentPortfolioREST()
        portfolio.run()
    except Exception as e:
        print(f"Критическая ошибка: {e}")


if __name__ == '__main__':
    main()