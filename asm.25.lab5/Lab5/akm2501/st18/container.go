package akm250118

import (
	"fmt"
	"strconv"
	"strings"
)

type GroupContainer struct {
	io      *ConsoleIO
	storage *RestStorage
}

func NewGroupContainer(io *ConsoleIO, storage *RestStorage) *GroupContainer {
	return &GroupContainer{io: io, storage: storage}
}

func (c *GroupContainer) AddItem() {
	fmt.Println("\nВыберите тип сотрудника:")
	fmt.Println("1. Worker\n2. Manager\n3. Director")

	choice := c.io.inputString("Ваш выбор (1/2/3): ")
	empData := make(map[string]interface{})
	empData["name"] = ""
	empData["age"] = 0

	switch choice {
	case "1":
		empData["type"] = "Worker"
		c.io.ReadField(empData, "name")
		c.io.ReadField(empData, "age")
		c.io.ReadField(empData, "department")
	case "2":
		empData["type"] = "Manager"
		c.io.ReadField(empData, "name")
		c.io.ReadField(empData, "age")
		c.io.ReadField(empData, "team_size")
	case "3":
		empData["type"] = "Director"
		c.io.ReadField(empData, "name")
		c.io.ReadField(empData, "age")
		c.io.ReadField(empData, "has_company_car")
	default:
		fmt.Println("Неизвестный тип.")
		return
	}

	employee, err := c.storage.Add(empData)
	if err != nil {
		fmt.Printf("Ошибка создания: %v\n", err)
		return
	}
	fmt.Println("\n✓ Добавлено.")
	c.printEmployee(employee, 0)
}

func (c *GroupContainer) ListItems() {
	employees, err := c.storage.ListItems()
	if err != nil {
		fmt.Printf("Ошибка получения списка: %v\n", err)
		return
	}
	if len(employees) == 0 {
		fmt.Println("Список пуст.")
		return
	}
	for i, emp := range employees {
		c.printEmployee(emp, i+1)
	}
}

func (c *GroupContainer) printEmployee(emp map[string]interface{}, index int) {
	if index > 0 {
		fmt.Printf("\n--- [%d] ---\n", index)
	}
	if id, ok := emp["id"].(float64); ok {
		fmt.Printf("ID: %.0f\n", id)
	}
	if typeName, ok := emp["type"].(string); ok {
		fmt.Printf("Тип: %s\n", typeName)
	}

	fields := []string{"name", "age"}
	typeName, _ := emp["type"].(string)
	switch typeName {
	case "Worker":
		fields = append(fields, "department")
	case "Manager":
		fields = append(fields, "team_size")
	case "Director":
		fields = append(fields, "has_company_car")
	}

	for _, field := range fields {
		if _, ok := emp[field]; ok {
			c.io.WriteField(emp, field)
		}
	}
	fmt.Println("---")
}

func (c *GroupContainer) selectIndex() (int, map[string]interface{}) {
	c.ListItems()
	raw := c.io.inputString("\nНомер объекта: ")
	idx, err := strconv.Atoi(raw)
	if err != nil {
		fmt.Println("Неверный номер.")
		return -1, nil
	}

	employees, err := c.storage.ListItems()
	if err != nil {
		return -1, nil
	}

	if idx < 1 || idx > len(employees) {
		fmt.Println("Неверный диапазон.")
		return -1, nil
	}

	emp := employees[idx-1]
	var itemID int
	if id, ok := emp["id"].(float64); ok {
		itemID = int(id)
	}
	return itemID, emp
}

func (c *GroupContainer) EditItem() {
	itemID, emp := c.selectIndex()
	if itemID < 0 {
		return
	}

	typeName, _ := emp["type"].(string)
	fmt.Printf("\nРедактирование сотрудника: %s (ID: %d)\n", typeName, itemID)

	fields := []string{"name", "age"}
	switch typeName {
	case "Worker":
		fields = append(fields, "department")
	case "Manager":
		fields = append(fields, "team_size")
	case "Director":
		fields = append(fields, "has_company_car")
	}

	fmt.Println("Доступные поля:")
	for i, field := range fields {
		fmt.Printf("%d. %s\n", i+1, c.io.label(field))
	}

	fieldChoice := c.io.inputString("Выберите поле для редактирования (1/2/3): ")
	fieldIdx, err := strconv.Atoi(fieldChoice)
	if err != nil || fieldIdx < 1 || fieldIdx > len(fields) {
		fmt.Println("Нет такого поля.")
		return
	}

	field := fields[fieldIdx-1]
	updates := make(map[string]interface{})
	c.io.ReadField(updates, field)

	err = c.storage.Patch(itemID, updates)
	if err != nil {
		fmt.Printf("Ошибка обновления: %v\n", err)
		return
	}
	fmt.Println("✓ Изменено.")
}

func (c *GroupContainer) RemoveItem() {
	itemID, emp := c.selectIndex()
	if itemID < 0 {
		return
	}

	err := c.storage.Remove(itemID)
	if err != nil {
		fmt.Printf("Ошибка удаления: %v\n", err)
		return
	}

	typeName, _ := emp["type"].(string)
	fmt.Printf("✓ Удалён %s.\n", typeName)
}

func (c *GroupContainer) Clear() {
	confirm := c.io.inputString("\nВы уверены? Это удалит всех сотрудников (да/нет): ")
	if !strings.HasPrefix(strings.ToLower(confirm), "д") && !strings.HasPrefix(strings.ToLower(confirm), "y") {
		fmt.Println("Отменено")
		return
	}

	count, err := c.storage.Clear()
	if err != nil {
		fmt.Printf("Ошибка очистки: %v\n", err)
		return
	}
	fmt.Printf("✓ Список очищен. Удалено: %d\n", count)
}
