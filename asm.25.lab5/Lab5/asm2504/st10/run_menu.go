package asm250410

import (
	"Lab5/rest"
	"fmt"
	"strings"
)

func RunMenu() {
	stID := GetStID()
	url := "http://127.0.0.1:5000/st" + strings.TrimSuffix(stID, "/") + "/api"
	fmt.Print(url)

	io := &ConsoleIO{}

	factoriesMap := map[string]func() Student{
		"Бакалавр": func() Student { return NewStudentBachelor() },
		"Магистр":  func() Student { return NewStudentMaster() },
		"Аспирант": func() Student { return NewStudentGraduate() },
	}
	typeNames := make([]string, 0, len(factoriesMap))
	for name := range factoriesMap {
		typeNames = append(typeNames, name)
	}

	gobStore := NewGobStorage()
	restStore := NewRESTStorage(url)
	cont := NewContainer(io, restStore)
	useREST := true

	for {
		io.Output("\nМеню:")
		io.Output("1. Добавить студента")
		io.Output("2. Редактировать студента")
		io.Output("3. Удалить студента")
		io.Output("4. Вывести весь список")
		io.Output("5. Сохранить в файл")
		io.Output("6. Загрузить из файла")
		io.Output("7. Очистить список")
		io.Output("8. Переключить стратегию хранения (локально/REST)")
		io.Output("0. Выход")

		choice := io.InputRaw("Выберите действие: ")
		switch choice {
		case "0":
			io.Output("Выход")
			return

		case "1":
			uiFactories := make([]func() Student, 0, len(typeNames))
			for _, n := range typeNames {
				if f, ok := factoriesMap[n]; ok {
					uiFactories = append(uiFactories, f)
				}
			}
			idx := io.SelectType(uiFactories)
			if idx < 0 || idx >= len(uiFactories) {
				break
			}
			obj := uiFactories[idx]()
			raw := io.InputFields(obj)

			newData := obj.GetData()
			valid := true
			for field, rawv := range raw {
				ok, val, errStr := obj.ValidateField(field, rawv)
				if !ok {
					io.Output(fmt.Sprintf("%s: %s", field, errStr))
					valid = false
					break
				}
				newData[field] = val
			}
			if !valid {
				break
			}
			obj.SetData(newData)
			if err := cont.Add(obj); err != nil {
				io.Output("Ошибка: " + err.Error())
			}

		case "2":
			rawItems, err := cont.Store.ListRaw()
			if err != nil {
				io.Output("Ошибка: " + err.Error())
				break
			}
			if len(rawItems) == 0 {
				io.Output("Список пуст")
				break
			}
			items := []Student{}
			rawIndexMap := []int{}
			for ri, r := range rawItems {
				if f, ok := factoriesMap[r.Class]; ok {
					obj := f()
					obj.SetData(r.Data)
					items = append(items, obj)
					rawIndexMap = append(rawIndexMap, ri)
				}
			}
			if len(items) == 0 {
				io.Output("Нет известных типов для отображения")
				break
			}
			sel := io.SelectIndex(items)
			if sel < 0 || sel >= len(items) {
				break
			}
			updates := io.InputUpdates(items[sel])
			if len(updates) == 0 {
				break
			}
			newData := map[string]interface{}{}
			for k, v := range items[sel].GetData() {
				newData[k] = v
			}
			valid := true
			for field, rawv := range updates {
				ok, val, errStr := items[sel].ValidateField(field, rawv)
				if !ok {
					io.Output(fmt.Sprintf("%s: %s", field, errStr))
					valid = false
					break
				}
				newData[field] = val
			}
			if !valid {
				break
			}
			items[sel].SetData(newData)
			if err := cont.UpdateByIndex(rawIndexMap[sel], items[sel]); err != nil {
				io.Output("Ошибка: " + err.Error())
			}

		case "3":
			rawItems, err := cont.Store.ListRaw()
			if err != nil {
				io.Output("Ошибка: " + err.Error())
				break
			}
			if len(rawItems) == 0 {
				io.Output("Список пуст")
				break
			}
			items := []Student{}
			rawIndexMap := []int{}
			for ri, r := range rawItems {
				if f, ok := factoriesMap[r.Class]; ok {
					obj := f()
					obj.SetData(r.Data)
					items = append(items, obj)
					rawIndexMap = append(rawIndexMap, ri)
				}
			}
			if len(items) == 0 {
				io.Output("Нет известных типов для отображения")
				break
			}
			sel := io.SelectIndex(items)
			if sel < 0 || sel >= len(items) {
				break
			}
			if err := cont.RemoveByIndex(rawIndexMap[sel]); err != nil {
				io.Output("Ошибка: " + err.Error())
			}

		case "4":
			items, err := cont.ListItems(factoriesMap)
			if err != nil {
				io.Output("Ошибка: " + err.Error())
				break
			}
			if len(items) == 0 {
				io.Output("Список пуст")
				break
			}
			for i, it := range items {
				io.Output(fmt.Sprintf("[%d] %s", i, it.String()))
			}

		case "5":
			fname := io.InputRaw("Имя файла для сохранения: ")
			if err := cont.SaveToFile(fname); err != nil {
				io.Output("Ошибка: " + err.Error())
			}

		case "6":
			fname := io.InputRaw("Имя файла для загрузки: ")
			if err := cont.LoadFromFile(fname, factoriesMap); err != nil {
				io.Output("Ошибка: " + err.Error())
			}

		case "7":
			if err := cont.Clear(); err != nil {
				io.Output("Ошибка: " + err.Error())
			}

		case "8":
			useREST = !useREST
			if useREST {
				cont.Store = restStore
			} else {
				cont.Store = gobStore
			}
			mode := "GobStorage"
			if useREST {
				mode = "RESTStorage"
			}
			io.Output("Стратегия хранения: " + mode)

		default:
			io.Output("Отсуствует данная функция")
		}
	}
}

func GetStID() string {
	resp := rest.DoRequest("GET", "", "", nil)
	raw := rest.GetAny(resp).(map[string]interface{})
	entries := raw["sts"].([]interface{})

	for _, e := range entries {
		arr := e.([]interface{})
		id := int(arr[0].(float64))
		title := arr[1].(string)
		if strings.Contains(title, "[2504-10]") {
			return fmt.Sprintf("%d", id)
		}
	}
	return ""
}
