package asm250406

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

/*
  console.go
  - функции для чтения ввода из консоли и редактирования Row через интерактивные подсказки
*/

// Общий reader для ввода
var in = bufio.NewReader(os.Stdin)

// ReadLine — прочитать строку с выводом prompt (trimmed)
func ReadLine(prompt string) string {
	fmt.Print(prompt)
	s, _ := in.ReadString('\n')
	return strings.TrimSpace(s)
}

// ReadStringPrompt — запрашивает строковое поле, возвращает указатель на строку (или существующую)
func ReadStringPrompt(prompt string, cur *string) *string {
	def := ""
	if cur != nil && *cur != "" {
		def = " [текущее: " + *cur + "]"
	}
	raw := ReadLine(prompt + def + ": ")
	if raw == "" {
		return cur
	}
	return &raw
}

// ReadFloatPrompt — запрашивает число float64, возвращает указатель или текущее значение
func ReadFloatPrompt(prompt string, cur *float64) *float64 {
	def := ""
	if cur != nil {
		def = fmt.Sprintf(" [текущее: %v]", *cur)
	}
	raw := ReadLine(prompt + def + ": ")
	if raw == "" {
		return cur
	}
	v, err := strconv.ParseFloat(raw, 64)
	if err != nil {
		fmt.Println("Неверный формат числа — оставляю текущее.")
		return cur
	}
	return &v
}

// ChooseKind — интерактивно выбрать тип ("camera" или "lens")
func ChooseKind() string {
	for {
		fmt.Println("1) Камера")
		fmt.Println("2) Объектив")
		ch := ReadLine("1/2: ")
		if ch == "1" {
			return "camera"
		}
		if ch == "2" {
			return "lens"
		}
		fmt.Println("Неверный выбор.")
	}
}

// InteractiveEdit: если existing != nil — использовать текущие значения как дефолты.
// forceKind если не пуст — принудительно задаёт тип ("camera" или "lens").
// Возвращает изменённую Row (копию).
func InteractiveEdit(existing *Row, forceKind string) Row {
	var r Row
	if existing != nil {
		r = *existing
	}
	kind := forceKind
	if kind == "" {
		kind = r.DetectType()
	}
	// Общие поля
	r.Type = &kind
	r.Manufacturer = ReadStringPrompt("Производитель", r.Manufacturer)
	r.Model = ReadStringPrompt("Модель", r.Model)
	r.Price = ReadFloatPrompt("Цена", r.Price)
	r.Weight = ReadFloatPrompt("Вес (грамм)", r.Weight)
	r.Bayonet = ReadStringPrompt("Байонет (mount)", r.Bayonet)

	if kind == "camera" {
		r.SensorSize = ReadStringPrompt("Размер матрицы", r.SensorSize)
		r.Megapixels = ReadFloatPrompt("Разрешение (МП)", r.Megapixels)
		// clear lens fields
		r.FocalLength = nil
		r.MaxAperture = nil
		r.MinAperture = nil
	} else {
		r.FocalLength = ReadStringPrompt("Фокусное расстояние", r.FocalLength)
		r.MaxAperture = ReadStringPrompt("Макс. диафрагма", r.MaxAperture)
		r.MinAperture = ReadStringPrompt("Мин. диафрагма", r.MinAperture)
		// clear camera fields
		r.SensorSize = nil
		r.Megapixels = nil
	}
	return r
}

// небольшая обёртка для atoi, чтобы избежать лишнего импорта в main.go
func strconvAtoi(s string) (int, error) {
	return strconv.Atoi(strings.TrimSpace(s))
}
