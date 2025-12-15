package akm250118

import (
	"fmt"
	"strconv"
	"strings"
)

type CardIndex struct {
	io      *ConsoleIO
	storage *RestStorage
}

func NewCardIndex(io *ConsoleIO, storage *RestStorage) *CardIndex {
	return &CardIndex{io: io, storage: storage}
}

func (c *CardIndex) AddItem() {
	fmt.Println("\nВыберите тип элемента:")
	fmt.Println("1. Student (Студент)")
	fmt.Println("2. Employee (Сотрудник)")
	
	choice := c.io.inputString("Ваш выбор (1/2): ")
	itemData := make(map[string]interface{})
	
	switch choice {
	case "1":
		itemData["type"] = "student"
		c.io.ReadField(itemData, "name")
		c.io.ReadField(itemData, "age")
		c.io.ReadField(itemData, "group_name")
	case "2":
		itemData["type"] = "employee"
		c.io.ReadField(itemData, "name")
		c.io.ReadField(itemData, "position")
	default:
		fmt.Println("Неизвестный тип.")
		return
	}
	
	newID, err := c.storage.Add(itemData)
	if err != nil {
		fmt.Printf("Ошибка добавления: %v\n", err)
		return
	}
	fmt.Printf("\n✓ Элемент добавлен с ID: %d\n", newID)
}

func (c *CardIndex) ListItems() {
	items, err := c.storage.ListItems()
	if err != nil {
		fmt.Printf("Ошибка получения списка: %v\n", err)
		return
	}
	if len(items) == 0 {
		fmt.Println("\nКартотека пуста.")
		return
	}
	
	fmt.Println("\n========== КАРТОТЕКА ==========")
	for i, item := range items {
		c.printItem(item, i+1)
	}
	fmt.Println("================================")
}

func (c *CardIndex) printItem(item map[string]interface{}, index int) {
	fmt.Printf("\n[%d] ", index)
	
	if id, ok := item["id"].(float64); ok {
		fmt.Printf("ID: %.0f", id)
	}
	
	if typeName, ok := item["type"].(string); ok {
		if typeName == "student" {
			fmt.Print(" | Студент")
		} else if typeName == "employee" {
			fmt.Print(" | Сотрудник")
		}
	}
	fmt.Println()
	
	// Определяем поля для вывода в зависимости от типа
	typeName, _ := item["type"].(string)
	var fields []string
	
	if typeName == "student" {
		fields = []string{"name", "age", "group_name"}
	} else if typeName == "employee" {
		fields = []string{"name", "position"}
	} else {
		fields = []string{"name"}
	}
	
	for _, field := range fields {
		if _, ok := item[field]; ok {
			c.io.WriteField(item, field)
		}
	}
	fmt.Println("---")
}

func (c *CardIndex) selectIndex() (int, map[string]interface{}) {
	c.ListItems()
	raw := c.io.inputString("\nВведите номер элемента: ")
	idx, err := strconv.Atoi(raw)
	if err != nil {
		fmt.Println("Неверный номер.")
		return -1, nil
	}
	
	items, err := c.storage.ListItems()
	if err != nil {
		fmt.Printf("Ошибка: %v\n", err)
		return -1, nil
	}
	
	if idx < 1 || idx > len(items) {
		fmt.Println("Номер вне диапазона.")
		return -1, nil
	}
	
	item := items[idx-1]
	var itemID int
	if id, ok := item["id"].(float64); ok {
		itemID = int(id)
	}
	return itemID, item
}

func (c *CardIndex) EditItem() {
	itemID, item := c.selectIndex()
	if itemID < 0 {
		return
	}
	
	typeName, _ := item["type"].(string)
	fmt.Printf("\nРедактирование элемента (ID: %d)\n", itemID)
	
	// Определяем доступные поля для редактирования
	var fields []string
	if typeName == "student" {
		fields = []string{"name", "age", "group_name"}
	} else if typeName == "employee" {
		fields = []string{"name", "position"}
	}
	
	fmt.Println("Доступные поля:")
	for i, field := range fields {
		fmt.Printf("%d. %s\n", i+1, c.io.label(field))
	}
	
	fieldChoice := c.io.inputString("Выберите поле для редактирования: ")
	fieldIdx, err := strconv.Atoi(fieldChoice)
	if err != nil || fieldIdx < 1 || fieldIdx > len(fields) {
		fmt.Println("Неверный выбор.")
		return
	}
	
	field := fields[fieldIdx-1]
	
	// Считываем текущие значения всех полей
	updatedData := make(map[string]interface{})
	updatedData["type"] = typeName
	
	// Копируем все существующие поля
	for _, f := range fields {
		if val, ok := item[f]; ok {
			updatedData[f] = val
		}
	}
	
	// Обновляем выбранное поле
	c.io.ReadField(updatedData, field)
	
	err = c.storage.Update(itemID, updatedData)
	if err != nil {
		fmt.Printf("Ошибка обновления: %v\n", err)
		return
	}
	fmt.Println("✓ Элемент успешно обновлён.")
}

func (c *CardIndex) RemoveItem() {
	itemID, item := c.selectIndex()
	if itemID < 0 {
		return
	}
	
	confirm := c.io.inputString("\nВы уверены? (да/нет): ")
	if !strings.HasPrefix(strings.ToLower(confirm), "д") && !strings.HasPrefix(strings.ToLower(confirm), "y") {
		fmt.Println("Отменено")
		return
	}
	
	err := c.storage.Remove(itemID)
	if err != nil {
		fmt.Printf("Ошибка удаления: %v\n", err)
		return
	}
	
	name := "Элемент"
	if n, ok := item["name"].(string); ok && n != "" {
		name = n
	}
	fmt.Printf("✓ Удалён: %s (ID: %d)\n", name, itemID)
}

func (c *CardIndex) Clear() {
	confirm := c.io.inputString("\nВы уверены? Это удалит ВСЕ элементы из картотеки! (да/нет): ")
	if !strings.HasPrefix(strings.ToLower(confirm), "д") && !strings.HasPrefix(strings.ToLower(confirm), "y") {
		fmt.Println("Отменено")
		return
	}
	
	err := c.storage.Clear()
	if err != nil {
		fmt.Printf("Ошибка очистки: %v\n", err)
		return
	}
	fmt.Println("✓ Картотека полностью очищена.")
}

