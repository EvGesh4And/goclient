package akm250114

import "fmt"

func Main() {
	fmt.Println("Картотека сотрудников (Worker / Manager / Director)")
	fmt.Println("Подключение к серверу...")

	io := NewConsoleIO()
	storage, err := NewRestStorage()
	if err != nil {
		fmt.Printf("Ошибка: %v\nУбедитесь, что WSGI-приложение запущено на http://127.0.0.1:5000\n", err)
		return
	}
	fmt.Printf("Маршрут: %s\n", storage.Prefix)

	container := NewGroupContainer(io, storage)

	for {
		fmt.Println("\n--- Меню ---")
		fmt.Println(" 1. Добавить объект")
		fmt.Println(" 2. Редактировать объект")
		fmt.Println(" 3. Удалить объект")
		fmt.Println(" 4. Вывести весь список")
		fmt.Println(" 5. Очистить список")
		fmt.Println(" 0. Выход")

		choice := io.inputString("\nВаш выбор: ")
		switch choice {
		case "0":
			fmt.Println("Пока!")
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
			fmt.Println("Нет такого пункта.")
		}
	}
}
