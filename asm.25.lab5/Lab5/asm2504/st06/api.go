package asm250406

import (
	"encoding/json"
	"fmt"
	"strings"

	"Lab5/rest"
)

/*
  api.go
  - структура Row (соответствует JSON "row" на сервере)
  - методы форматирования и детекции типа
  - функции-обёртки для REST (listRows, getRow, addRow, updateRow, deleteRow, clearAll)
*/

// Row соответствует JSON-строке, которую отдаёт/принимает сервер.
type Row struct {
	Type         *string  `json:"type,omitempty"`
	Manufacturer *string  `json:"manufacturer,omitempty"`
	Model        *string  `json:"model,omitempty"`
	Price        *float64 `json:"price,omitempty"`
	Weight       *float64 `json:"weight,omitempty"`
	Bayonet      *string  `json:"bayonet,omitempty"`

	SensorSize   *string  `json:"sensor_size,omitempty"`
	Megapixels   *float64 `json:"megapixels,omitempty"`

	FocalLength  *string  `json:"focal_length,omitempty"`
	MaxAperture  *string  `json:"max_aperture,omitempty"`
	MinAperture  *string  `json:"min_aperture,omitempty"`
}

// Вспомогательные функции для безопасного разворачивания указателей
func s(v *string) string {
	if v == nil {
		return ""
	}
	return *v
}
func f(v *float64) float64 {
	if v == nil {
		return 0
	}
	return *v
}

// DetectType возвращает "camera" или "lens" исходя из полей Row.
// Если явно задано поле Type — оно имеет приоритет.
func (r *Row) DetectType() string {
	if r == nil {
		return "camera"
	}
	if r.Type != nil && *r.Type != "" {
		return *r.Type
	}
	if r.FocalLength != nil && strings.TrimSpace(*r.FocalLength) != "" {
		return "lens"
	}
	if r.MaxAperture != nil && strings.TrimSpace(*r.MaxAperture) != "" {
		return "lens"
	}
	return "camera"
}

// Summary возвращает краткую строку для списка элементов
func (r *Row) Summary() string {
	if r == nil {
		return ""
	}
	if r.DetectType() == "camera" {
		return fmt.Sprintf("%s %vMP", s(r.Manufacturer), f(r.Megapixels))
	}
	return fmt.Sprintf("%s %s", s(r.Manufacturer), s(r.FocalLength))
}

// PrettyFull возвращает многострочное представление для детального вывода
func (r *Row) PrettyFull() string {
	if r == nil {
		return "<nil>"
	}
	var sb strings.Builder
	fmt.Fprintf(&sb, "Type: %s\n", r.DetectType())
	fmt.Fprintf(&sb, "Manufacturer: %s\n", s(r.Manufacturer))
	fmt.Fprintf(&sb, "Model: %s\n", s(r.Model))
	fmt.Fprintf(&sb, "Price: %v\n", f(r.Price))
	fmt.Fprintf(&sb, "Weight: %v\n", f(r.Weight))
	fmt.Fprintf(&sb, "Bayonet: %s\n", s(r.Bayonet))
	if r.DetectType() == "camera" {
		fmt.Fprintf(&sb, "Sensor size: %s\n", s(r.SensorSize))
		fmt.Fprintf(&sb, "Megapixels: %v\n", f(r.Megapixels))
	} else {
		fmt.Fprintf(&sb, "Focal length: %s\n", s(r.FocalLength))
		fmt.Fprintf(&sb, "Max aperture: %s\n", s(r.MaxAperture))
		fmt.Fprintf(&sb, "Min aperture: %s\n", s(r.MinAperture))
	}
	return sb.String()
}

// ---------- REST helpers (используют Lab5/rest) ----------

// listRows — получает список рядов (rows) с сервера (GET /stPrefix/api/items)
func listRows() ([]Row, error) {
	body := rest.DoRequest("GET", stPrefix, "items", nil)
	if body == nil {
		return nil, fmt.Errorf("no response body")
	}
	// получаем байты и распаковываем в []Row
	b := rest.GetBytes(body)
	var rows []Row
	if err := json.Unmarshal(b, &rows); err != nil {
		return nil, err
	}
	return rows, nil
}

// getRow — получить один row по offset idx (GET /stPrefix/api/items/{idx})
func getRow(idx int) (*Row, error) {
	cmd := fmt.Sprintf("items/%d", idx)
	body := rest.DoRequest("GET", stPrefix, cmd, nil)
	if body == nil {
		return nil, fmt.Errorf("no response")
	}
	var r Row
	ok := rest.GetDecoded(body, &r)
	if !ok {
		return nil, fmt.Errorf("cannot decode response")
	}
	return &r, nil
}

// addRow — добавить row (POST /stPrefix/api/items). Возвращает id/offset от сервера.
func addRow(r Row) (int, error) {
	body := rest.DoRequest("POST", stPrefix, "items", r)
	if body == nil {
		return 0, fmt.Errorf("no response from server")
	}
	var resp map[string]any
	ok := rest.GetDecoded(body, &resp)
	if !ok {
		return 0, fmt.Errorf("cannot decode add response")
	}
	if idv, has := resp["id"]; has {
		switch v := idv.(type) {
		case float64:
			return int(v), nil
		case int:
			return v, nil
		}
	}
	return 0, fmt.Errorf("id not returned")
}

// updateRow — обновить по idx (PUT /stPrefix/api/items/{idx})
func updateRow(idx int, r Row) error {
	cmd := fmt.Sprintf("items/%d", idx)
	body := rest.DoRequest("PUT", stPrefix, cmd, r)
	// rest.DoRequest при пустом ответе вернёт nil — считаем это ok
	if body == nil {
		return nil
	}
	// пробуем прочитать возможный JSON с {"ok":true} или ошибку
	var resp map[string]any
	rest.GetDecoded(body, &resp)
	return nil
}

// deleteRow — удалить (DELETE /stPrefix/api/items/{idx})
func deleteRow(idx int) error {
	cmd := fmt.Sprintf("items/%d", idx)
	body := rest.DoRequest("DELETE", stPrefix, cmd, nil)
	if body == nil {
		// assume ok
		return nil
	}
	var resp map[string]any
	rest.GetDecoded(body, &resp)
	return nil
}

// clearAll — удаляет все элементы, вызывая deleteRow для каждого (с конца)
func clearAll() error {
	rows, err := listRows()
	if err != nil {
		return err
	}
	// удаляем с конца
	for i := len(rows) - 1; i >= 0; i-- {
		if err := deleteRow(i); err != nil {
			fmt.Printf("warning: delete %d failed: %v\n", i, err)
		}
	}
	return nil
}
