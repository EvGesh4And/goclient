package asm250410

type StoredEntry struct {
	Class string
	Data  map[string]interface{}
}

type Storage interface {
	ListRaw() ([]StoredEntry, error)
	AddRaw(StoredEntry) error
	UpdateRaw(int, StoredEntry) error
	RemoveRaw(int) (StoredEntry, error)
	Clear() error
	SaveToFile(string) error
	LoadFromFile(string) error
}
