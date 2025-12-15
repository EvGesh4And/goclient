package main

import (
	"fmt"
	"sort"

	// добавить импорт своего пакета по шаблону
	// <код группы><номер по журналу>  "Lab5/<код группы>/st<номер по журналу>"
	akm250100 "Lab5/akm2501/st00"
	akm250114 "Lab5/akm2501/st14"
	akm250118 "Lab5/akm2501/st18"
	asm250400 "Lab5/asm2504/st00"
	asm250406 "Lab5/asm2504/st06"
	asm250410 "Lab5/asm2504/st10"
)

var menuItems = []struct {
	title string
	f     func()
}{
	// добавить пункт меню для вызова своей стартовой функции
	{"[2501-00] Образец 2501", akm250100.Main},
	{"[2501-14] Погосян", akm250114.Main},
	{"[2501-18] Группа акм2501", akm250118.Main},
	{"[2504-00] Образец 2504", asm250400.Main},
	{"[2504-10] Князев", asm250410.Main},
	{"[2504-16] Галимов", asm250406.Main},
}

func menu() bool {
	for i, m := range menuItems {
		fmt.Println(i+1, m.title)
	}

	var i int
	if _, e := fmt.Scanln(&i); e != nil || i < 1 || i > len(menuItems) {
		return false
	}

	menuItems[i-1].f()
	return true
}

func main() {
	sort.Slice(menuItems, func(i, j int) bool {
		return menuItems[i].title < menuItems[j].title
	})
	for menu() {
	}
}
