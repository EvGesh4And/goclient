package asm250410

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
	"time"
)

type RESTStorage struct {
	BaseURL string
	Client  *http.Client
}

func NewRESTStorage(baseURL string) *RESTStorage {
	return &RESTStorage{
		BaseURL: strings.TrimRight(baseURL, "/"),
		Client:  &http.Client{Timeout: 5 * time.Second},
	}
}

func (r *RESTStorage) ListRaw() ([]StoredEntry, error) {
	resp, err := r.Client.Get(r.BaseURL + "/members")
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	b, _ := io.ReadAll(resp.Body)
	var raw []map[string]interface{}
	if err := json.Unmarshal(b, &raw); err != nil {
		return nil, err
	}
	out := []StoredEntry{}
	for _, e := range raw {
		cls, _ := e["__class__"].(string)
		data, _ := e["data"].(map[string]interface{})
		out = append(out, StoredEntry{Class: cls, Data: data})
	}
	return out, nil
}

func (r *RESTStorage) AddRaw(e StoredEntry) error {
	entry := map[string]interface{}{"__class__": e.Class, "data": e.Data}
	b, _ := json.Marshal(entry)
	resp, err := r.Client.Post(r.BaseURL+"/members/add", "application/json", bytes.NewReader(b))
	if err != nil {
		return err
	}
	resp.Body.Close()
	if resp.StatusCode >= 400 {
		return fmt.Errorf("status %d", resp.StatusCode)
	}
	return nil
}

func (r *RESTStorage) RemoveRaw(index int) (StoredEntry, error) {
	req, _ := http.NewRequest("DELETE", fmt.Sprintf("%s/members/remove/%d", r.BaseURL, index), nil)
	resp, err := r.Client.Do(req)
	if err != nil {
		return StoredEntry{}, err
	}
	defer resp.Body.Close()
	if resp.StatusCode == 404 {
		return StoredEntry{}, fmt.Errorf("index out of range")
	}
	if resp.StatusCode >= 400 {
		return StoredEntry{}, fmt.Errorf("status %d", resp.StatusCode)
	}
	var out map[string]interface{}
	b, _ := io.ReadAll(resp.Body)
	json.Unmarshal(b, &out)
	rem, _ := out["removed"].(map[string]interface{})
	cls, _ := rem["__class__"].(string)
	data, _ := rem["data"].(map[string]interface{})
	return StoredEntry{Class: cls, Data: data}, nil
}

func (r *RESTStorage) UpdateRaw(index int, e StoredEntry) error {
	entry := map[string]interface{}{"__class__": e.Class, "data": e.Data}
	b, _ := json.Marshal(entry)
	req, _ := http.NewRequest("PUT", fmt.Sprintf("%s/members/edit/%d", r.BaseURL, index), bytes.NewReader(b))
	req.Header.Set("Content-Type", "application/json")
	resp, err := r.Client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	if resp.StatusCode == 404 {
		return fmt.Errorf("index out of range")
	}
	if resp.StatusCode >= 400 {
		return fmt.Errorf("status %d", resp.StatusCode)
	}
	return nil
}

func (r *RESTStorage) Clear() error {
	req, _ := http.NewRequest("POST", r.BaseURL+"/members/clear_list", strings.NewReader("[]"))
	resp, err := r.Client.Do(req)
	if err != nil {
		return err
	}
	resp.Body.Close()
	return nil
}

func (r *RESTStorage) SaveToFile(string) error {
	return fmt.Errorf("SaveToFile not supported for RESTStorage")
}
func (r *RESTStorage) LoadFromFile(string) error {
	return fmt.Errorf("LoadFromFile not supported for RESTStorage")
}
