package akm250118

import (
	"Lab5/rest"
	"encoding/json"
	"fmt"
	"io"
	"strings"
)

type RestStorage struct {
	Prefix string
}

func NewRestStorage() (*RestStorage, error) {
	prefix, err := detectPrefix()
	if err != nil {
		return nil, err
	}
	return &RestStorage{Prefix: prefix}, nil
}

func detectPrefix() (string, error) {
	body := rest.GetAny(rest.DoRequest("GET", "", "", nil))
	if body == nil {
		return "", fmt.Errorf("не удалось получить список модулей")
	}
	data, ok := body.(map[string]interface{})
	if !ok {
		return "", fmt.Errorf("неверный формат ответа от сервера")
	}
	sts, _ := data["sts"].([]interface{})
	for _, st := range sts {
		stArr, ok := st.([]interface{})
		if !ok || len(stArr) < 2 {
			continue
		}
		if id, ok := stArr[0].(float64); ok {
			if title, ok := stArr[1].(string); ok && strings.Contains(title, "[2501-18]") {
				return fmt.Sprintf("st%d/", int(id)), nil
			}
		}
	}
	return "", fmt.Errorf("не удалось найти модуль [2501-18]")
}

func decodeJSON(body io.ReadCloser) (map[string]interface{}, error) {
	if body == nil {
		return nil, fmt.Errorf("пустой ответ от сервера")
	}
	var result map[string]interface{}
	err := json.NewDecoder(body).Decode(&result)
	body.Close()
	if err != nil {
		return nil, fmt.Errorf("ошибка декодирования: %v", err)
	}
	return result, nil
}

func decodeList(body io.ReadCloser) ([]map[string]interface{}, error) {
	if body == nil {
		return nil, fmt.Errorf("пустой ответ от сервера")
	}
	var resp EmployeeListResponse
	err := json.NewDecoder(body).Decode(&resp)
	body.Close()
	if err != nil {
		return nil, fmt.Errorf("ошибка декодирования: %v", err)
	}
	return resp.Employees, nil
}

func (s *RestStorage) ListItems() ([]map[string]interface{}, error) {
	return decodeList(rest.DoRequest("GET", s.Prefix, "employees", nil))
}

func (s *RestStorage) Get(itemID int) (map[string]interface{}, error) {
	return decodeJSON(rest.DoRequest("GET", s.Prefix, fmt.Sprintf("employees/%d", itemID), nil))
}

func (s *RestStorage) Add(empData map[string]interface{}) (map[string]interface{}, error) {
	return decodeJSON(rest.DoRequest("POST", s.Prefix, "employees", empData))
}

func (s *RestStorage) Update(itemID int, empData map[string]interface{}) error {
	body := rest.DoRequest("PUT", s.Prefix, fmt.Sprintf("employees/%d", itemID), empData)
	if body != nil {
		body.Close()
	}
	return nil
}

func (s *RestStorage) Patch(itemID int, empData map[string]interface{}) error {
	body := rest.DoRequest("PATCH", s.Prefix, fmt.Sprintf("employees/%d", itemID), empData)
	if body != nil {
		body.Close()
	}
	return nil
}

func (s *RestStorage) Remove(itemID int) error {
	body := rest.DoRequest("DELETE", s.Prefix, fmt.Sprintf("employees/%d", itemID), nil)
	if body != nil {
		body.Close()
	}
	return nil
}

func (s *RestStorage) Clear() (int, error) {
	body := rest.DoRequest("DELETE", s.Prefix, "employees", nil)
	if body == nil {
		return 0, fmt.Errorf("пустой ответ от сервера")
	}
	var resp ClearResponse
	err := json.NewDecoder(body).Decode(&resp)
	body.Close()
	if err != nil {
		return 0, fmt.Errorf("ошибка декодирования: %v", err)
	}
	return resp.Removed, nil
}
