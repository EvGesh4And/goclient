package akm250118

import "fmt"

func Main() {
	fmt.Println("Картотека (Student / Employee)")
	fmt.Println("Подключение к серверу...")

	io := NewConsoleIO()
	storage, err := NewRestStorage()
	if err != nil {
		fmt.Printf("Ошибка: %v\nУбедитесь, что WSGI-приложение запущено на http://127.0.0.1:5000\n", err)
		return
	}
	fmt.Printf("Маршрут: %s\n", storage.Prefix)

	container := NewCardIndex(io, storage)

	for {
		fmt.Println("\n--- Меню ---")
		fmt.Println(" 1. Добавить элемент")
		fmt.Println(" 2. Редактировать элемент")
		fmt.Println(" 3. Удалить элемент")
		fmt.Println(" 4. Показать все элементы")
		fmt.Println(" 5. Очистить картотеку")
		fmt.Println(" 0. Выход")

		choice := io.inputString("\nВаш выбор: ")
		switch choice {
		case "0":
			fmt.Println("До свидания!")
			return
		case "1":
			container.AddItem()
		case "2":
			container.EditItem()
		case "3":
			container.RemoveItem()
		case "4":
			container.ListItems()
		case "5":
			container.Clear()
		default:
			fmt.Println("Неизвестный пункт меню.")
		}
	}
}

