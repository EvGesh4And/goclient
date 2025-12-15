package akm250118

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type ConsoleIO struct {
	reader *bufio.Reader
}

func NewConsoleIO() *ConsoleIO {
	return &ConsoleIO{reader: bufio.NewReader(os.Stdin)}
}

var fieldLabels = map[string]string{
	"name":       "Имя",
	"age":        "Возраст",
	"group_name": "Группа",
	"position":   "Должность",
}

func (io *ConsoleIO) label(fieldName string) string {
	if label, ok := fieldLabels[fieldName]; ok {
		return label
	}
	return fieldName
}

func (io *ConsoleIO) convert(text string, fieldType string) interface{} {
	text = strings.TrimSpace(text)

	switch fieldType {
	case "int":
		if val, err := strconv.Atoi(text); err == nil {
			return val
		}
		return 0
	default:
		return text
	}
}

func (io *ConsoleIO) formatValue(value interface{}) string {
	if value == nil {
		return "—"
	}
	switch v := value.(type) {
	case string:
		if v == "" {
			return "—"
		}
	case float64:
		return fmt.Sprintf("%.0f", v)
	}
	return fmt.Sprintf("%v", value)
}

func (io *ConsoleIO) inputString(prompt string) string {
	fmt.Print(prompt)
	text, _ := io.reader.ReadString('\n')
	return strings.TrimSpace(text)
}

func (io *ConsoleIO) ReadField(item map[string]interface{}, fieldName string) {
	label := io.label(fieldName)

	var fieldType string
	switch fieldName {
	case "name", "group_name", "position":
		fieldType = "string"
	case "age":
		fieldType = "int"
	}

	prompt := fmt.Sprintf("Введите %s: ", label)
	text := io.inputString(prompt)
	value := io.convert(text, fieldType)
	item[fieldName] = value
}

func (io *ConsoleIO) WriteField(item map[string]interface{}, fieldName string) {
	label := io.label(fieldName)
	value := item[fieldName]
	fmt.Printf("%s: %s\n", label, io.formatValue(value))
}

