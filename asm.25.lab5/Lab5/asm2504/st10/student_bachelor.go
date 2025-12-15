package asm250410

import (
	"fmt"
	"strconv"
	"strings"
)

type StudentBachelor struct {
	data   map[string]interface{}
	fields []FieldDef
}

func NewStudentBachelor() *StudentBachelor {
	fields := []FieldDef{
		{"full_name", "ФИО"},
		{"age", "Возраст"},
		{"group", "Название группы"},
		{"gpa", "Средний балл"},
		{"diploma_topic", "Тема дипломной работы"},
	}
	d := make(map[string]interface{}, len(fields))
	for _, f := range fields {
		d[f.Key] = nil
	}
	return &StudentBachelor{data: d, fields: fields}
}

func (s *StudentBachelor) TypeName() string                 { return "Бакалавр" }
func (s *StudentBachelor) Fields() []FieldDef               { return s.fields }
func (s *StudentBachelor) GetData() map[string]interface{}  { return s.data }
func (s *StudentBachelor) SetData(d map[string]interface{}) { s.data = d }

type fieldHolder interface {
	Fields() []FieldDef
	Data() map[string]interface{}
	TypeName() string
}

func formatString(h fieldHolder) string {
	parts := ""
	for _, f := range h.Fields() {
		parts += fmt.Sprintf("%s: %v, ", f.Label, h.Data()[f.Key])
	}
	if len(parts) >= 2 {
		parts = parts[:len(parts)-2]
	}
	return fmt.Sprintf("%s (%s)", h.TypeName(), parts)
}

func (s *StudentBachelor) Data() map[string]interface{} { return s.data }
func (s *StudentBachelor) String() string               { return formatString(s) }

func (s *StudentBachelor) ValidateField(name, raw string) (bool, interface{}, string) {
	switch name {
	case "age":
		if strings.TrimSpace(raw) == "" {
			return false, nil, "Поле не может быть пустым"
		}
		v, err := strconv.Atoi(raw)
		if err != nil {
			return false, nil, "Ожидалось целое число"
		}
		if v < 1 || v > 150 {
			return false, nil, "Возраст должен быть в диапазоне 1-150"
		}
		return true, v, ""
	case "gpa":
		if strings.TrimSpace(raw) == "" {
			return false, nil, "Поле не может быть пустым"
		}
		r := strings.ReplaceAll(raw, ",", ".")
		f, err := strconv.ParseFloat(r, 64)
		if err != nil {
			return false, nil, "Ожидалось число"
		}
		if f < 0.0 || f > 5.0 {
			return false, nil, "Средний балл должен быть в диапазоне 0.0-5.0"
		}
		return true, f, ""
	default:
		if strings.TrimSpace(raw) == "" {
			return false, nil, "Поле не может быть пустым"
		}
		return true, raw, ""
	}
}
