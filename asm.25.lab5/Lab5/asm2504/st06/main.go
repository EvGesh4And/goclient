package asm250406

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
)


const labSubstring = "[2504-06]" 
var stPrefix string

func init() {
	res, err := http.Get("http://127.0.0.1:5000/api/")
	if err != nil {
		fmt.Println("Ошибка запроса /api/:", err)
		return
	}
	defer res.Body.Close()

	body, _ := io.ReadAll(res.Body)
	var data map[string]any
	if err := json.Unmarshal(body, &data); err != nil {
		fmt.Println("Ошибка разбора JSON /api/:", err)
		return
	}

	sts, ok := data["sts"].([]any)
	if !ok {
		fmt.Println("Ошибка: нет поля sts или неверный формат в /api/")
		return
	}

	for _, st := range sts {
		item, ok := st.([]any)
		if !ok || len(item) < 2 {
			continue
		}
		id := int(item[0].(float64))
		title := item[1].(string)
		if strings.Contains(title, labSubstring) {
			stPrefix = fmt.Sprintf("st%d/", id)
			break
		}
	}
	if stPrefix == "" {
		fmt.Println("Не найдено соответствие для", labSubstring, " — stPrefix останется пустым.")
	}
}


func Main() {
	fmt.Println("ASM2504-ST06 — Go REST client")
	for {
		fmt.Println()
		fmt.Println("1) Добавить объект")
		fmt.Println("2) Редактировать объект")
		fmt.Println("3) Удалить объект")
		fmt.Println("4) Вывести краткий список")
		fmt.Println("5) Вывести полный список")
		fmt.Println("8) Очистить список")
		fmt.Println("0) Выход")
		choice := ReadLine("Выбор: ")
		switch choice {
		case "0":
			return
		case "1":
			kind := ChooseKind()
			var r Row
			r.Type = &kind
			r = InteractiveEdit(&r, kind)
			id, err := addRow(r)
			if err != nil {
				fmt.Println("Ошибка добавления:", err)
			} else {
				fmt.Println("Добавлено. id/offset:", id)
			}
		case "2":
			rows, err := listRows()
			if err != nil {
				fmt.Println("Ошибка:", err)
				continue
			}
			if len(rows) == 0 {
				fmt.Println("<пусто>")
				continue
			}
			for i, rr := range rows {
				fmt.Printf("%d) [%s] %s\n", i+1, rr.DetectType(), rr.Summary())
			}
			raw := ReadLine("Номер для редактирования: ")
			n, err := strconvAtoi(raw)
			if err != nil || n < 1 || n > len(rows) {
				fmt.Println("Неверный номер.")
				continue
			}
			idx := n - 1
			existing := rows[idx]
			kind := existing.DetectType()
			edited := InteractiveEdit(&existing, kind)
			if err := updateRow(idx, edited); err != nil {
				fmt.Println("Ошибка обновления:", err)
			} else {
				fmt.Println("Обновлено.")
			}
		case "3":
			rows, err := listRows()
			if err != nil {
				fmt.Println("Ошибка:", err)
				continue
			}
			if len(rows) == 0 {
				fmt.Println("<пусто>")
				continue
			}
			for i, rr := range rows {
				fmt.Printf("%d) [%s] %s\n", i+1, rr.DetectType(), rr.Summary())
			}
			raw := ReadLine("Номер для удаления: ")
			n, err := strconvAtoi(raw)
			if err != nil || n < 1 || n > len(rows) {
				fmt.Println("Неверный номер.")
				continue
			}
			idx := n - 1
			if err := deleteRow(idx); err != nil {
				fmt.Println("Ошибка удаления:", err)
			} else {
				fmt.Println("Удалено.")
			}
		case "4":
			rows, err := listRows()
			if err != nil {
				fmt.Println("Ошибка:", err)
				continue
			}
			if len(rows) == 0 {
				fmt.Println("<пусто>")
				continue
			}
			for i, rr := range rows {
				fmt.Printf("%d) [%s] %s\n", i+1, rr.DetectType(), rr.Summary())
			}
		case "5":
			rows, err := listRows()
			if err != nil {
				fmt.Println("Ошибка:", err)
				continue
			}
			if len(rows) == 0 {
				fmt.Println("<пусто>")
				continue
			}
			for i, rr := range rows {
				fmt.Printf("\n=== Элемент %d ===\n%s\n", i+1, rr.PrettyFull())
			}
		case "8":
			confirm := ReadLine("Очистить весь список? Введите YES для подтверждения: ")
			if confirm == "YES" {
				if err := clearAll(); err != nil {
					fmt.Println("Ошибка очистки:", err)
				} else {
					fmt.Println("Список очищен.")
				}
			} else {
				fmt.Println("Отмена.")
			}
		default:
			fmt.Println("Неверный пункт.")
		}
	}
}
