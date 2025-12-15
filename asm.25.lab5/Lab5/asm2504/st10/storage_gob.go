package asm250410

import (
	"encoding/gob"
	"os"
)

type GobStorage struct {
	Items []StoredEntry
}

func NewGobStorage() *GobStorage {
	return &GobStorage{Items: []StoredEntry{}}
}

func (s *GobStorage) ListRaw() ([]StoredEntry, error) {
	return append([]StoredEntry(nil), s.Items...), nil
}

func (s *GobStorage) AddRaw(e StoredEntry) error {
	s.Items = append(s.Items, e)
	return nil
}

func (s *GobStorage) UpdateRaw(index int, e StoredEntry) error {
	if index < 0 || index >= len(s.Items) {
		return os.ErrInvalid
	}
	s.Items[index] = e
	return nil
}

func (s *GobStorage) RemoveRaw(index int) (StoredEntry, error) {
	if index < 0 || index >= len(s.Items) {
		return StoredEntry{}, os.ErrInvalid
	}
	removed := s.Items[index]
	s.Items = append(s.Items[:index], s.Items[index+1:]...)
	return removed, nil
}

func (s *GobStorage) Clear() error {
	s.Items = []StoredEntry{}
	return nil
}

func (s *GobStorage) SaveToFile(filename string) error {
	f, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer f.Close()
	enc := gob.NewEncoder(f)
	return enc.Encode(s.Items)
}

func (s *GobStorage) LoadFromFile(filename string) error {
	f, err := os.Open(filename)
	if err != nil {
		return err
	}
	defer f.Close()
	dec := gob.NewDecoder(f)
	var items []StoredEntry
	if err := dec.Decode(&items); err != nil {
		return err
	}
	s.Items = items
	return nil
}
