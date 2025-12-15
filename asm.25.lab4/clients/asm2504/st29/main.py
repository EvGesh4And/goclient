# clients/asm2504/st29/main.py
import sys
import os

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from console_client import InvestmentPortfolioREST

def main():
    """Основная функция запуска клиента"""
    try:
        print("Консольный клиент инвестиционного портфеля (REST API)")
        print("=" * 50)
        portfolio = InvestmentPortfolioREST()
        portfolio.run()
    except KeyboardInterrupt:
        print("\n\nПрограмма завершена пользователем.")
    except Exception as e:
        print(f"\nОшибка: {e}")

if __name__ == "__main__":
    main()