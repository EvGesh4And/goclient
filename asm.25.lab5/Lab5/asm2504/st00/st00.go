package asm250400

import (
	"Lab5/rest"
	"fmt"
)

func getList() {
	sts := rest.GetAny(rest.DoRequest("GET", "", "", nil)).(map[string]any)["sts"]
	for _, st := range sts.([]any) {
		id := int(st.([]any)[0].(float64))
		title := st.([]any)[1].(string)
		fmt.Println(id, title)
	}
}

type stItem struct {
	St string `json:"st"`
}

func Main() {
	fmt.Println("asm250400")
	getList()

	bytes := rest.GetBytes(rest.DoRequest("GET", "st1/", "", nil))
	fmt.Println(string(bytes))

	var st *stItem
	// json.Unmarshal(bytes, &st)
	rest.GetDecoded(rest.DoRequest("GET", "st1/", "", nil), &st)
	fmt.Println(st.St)
}
