package asm250410

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func parseIntSafe(s string) (int, error) {
	return strconv.Atoi(strings.TrimSpace(s))
}

var rdr = bufio.NewReader(os.Stdin)

func readLine(prompt string) string {
	fmt.Print(prompt)
	s, _ := rdr.ReadString('\n')
	return strings.TrimSpace(s)
}

type ConsoleIO struct{}

func (c *ConsoleIO) Output(msg string)             { fmt.Println(msg) }
func (c *ConsoleIO) InputRaw(prompt string) string { return readLine(prompt) }

func (c *ConsoleIO) SelectType(factories []func() Student) int {
	parts := []string{}
	for i, f := range factories {
		tmp := f()
		parts = append(parts, fmt.Sprintf("%d - %s", i+1, tmp.TypeName()))
	}
	fmt.Println("Выберите тип:", strings.Join(parts, ", "))
	s := readLine("Тип (номер): ")
	if s == "" {
		c.Output("Отмена или неверный ввод")
		return -1
	}
	idx, err := parseIntSafe(s)
	if err != nil || idx < 1 || idx > len(factories) {
		c.Output("Отмена или неверный ввод")
		return -1
	}
	return idx - 1
}

func (c *ConsoleIO) InputFields(obj Student) map[string]string {
	res := map[string]string{}
	fields := obj.Fields()
	for _, f := range fields {
		cur := obj.GetData()[f.Key]
		prompt := f.Label + ": "
		if cur != nil {
			prompt = fmt.Sprintf("%s [%v]: ", f.Label, cur)
		}
		for {
			raw := readLine(prompt)
			ok, _, errStr := obj.ValidateField(f.Key, raw)
			if ok {
				res[f.Key] = raw
				break
			}
			c.Output("Ошибка: " + errStr + ". Попробуйте ещё раз")
		}
	}
	return res
}

func (c *ConsoleIO) SelectIndex(items []Student) int {
	if len(items) == 0 {
		c.Output("Список пуст")
		return -1
	}
	for i, it := range items {
		fmt.Printf("[%d] %s\n", i, it.String())
	}
	s := readLine("Индекс для редактирования: ")
	if s == "" {
		c.Output("Отмена или неверный ввод")
		return -1
	}
	idx, err := parseIntSafe(s)
	if err != nil || idx < 0 || idx >= len(items) {
		c.Output("Номер вне диапазона")
		return -1
	}
	return idx
}

func (c *ConsoleIO) InputUpdates(obj Student) map[string]string {
	fields := obj.Fields()
	for i, f := range fields {
		fmt.Printf("%d. %s\n", i+1, f.Label)
	}
	s := readLine("Введите номер поля для редактирования (пусто — отмена): ")
	if s == "" {
		return nil
	}
	idx, err := parseIntSafe(s)
	if err != nil || idx < 1 || idx > len(fields) {
		c.Output("Ожидался номер поля")
		return nil
	}
	field := fields[idx-1]
	cur := obj.GetData()[field.Key]
	prompt := field.Label + ": "
	if cur != nil {
		prompt = fmt.Sprintf("%s [%v]: ", field.Label, cur)
	}
	for {
		raw := readLine(prompt)
		ok, _, errStr := obj.ValidateField(field.Key, raw)
		if ok {
			return map[string]string{field.Key: raw}
		}
		c.Output("Ошибка: " + errStr + ". Попробуйте ещё раз")
	}
}
