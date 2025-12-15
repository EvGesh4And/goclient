package akm250114

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
	"name":            "Имя",
	"age":             "Возраст",
	"department":      "Отдел",
	"team_size":       "Размер команды",
	"has_company_car": "Служебный автомобиль",
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
	case "bool":
		t := strings.ToLower(text)
		return t == "да" || t == "д" || t == "yes" || t == "y" || t == "true" || t == "1"
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
	case bool:
		if v {
			return "да"
		}
		return "нет"
	case string:
		if v == "" {
			return "—"
		}
	}
	return fmt.Sprintf("%v", value)
}

func (io *ConsoleIO) inputString(prompt string) string {
	fmt.Print(prompt)
	text, _ := io.reader.ReadString('\n')
	return strings.TrimSpace(text)
}

func (io *ConsoleIO) ReadField(emp map[string]interface{}, fieldName string) {
	label := io.label(fieldName)

	var fieldType string
	switch fieldName {
	case "name", "department":
		fieldType = "string"
	case "age", "team_size":
		fieldType = "int"
	case "has_company_car":
		fieldType = "bool"
	}

	var prompt string
	if fieldType == "bool" {
		prompt = fmt.Sprintf("%s (да/нет): ", label)
	} else {
		prompt = fmt.Sprintf("Введите %s: ", label)
	}

	text := io.inputString(prompt)
	value := io.convert(text, fieldType)
	emp[fieldName] = value
}

func (io *ConsoleIO) WriteField(emp map[string]interface{}, fieldName string) {
	label := io.label(fieldName)
	value := emp[fieldName]
	fmt.Printf("%s: %s\n", label, io.formatValue(value))
}
