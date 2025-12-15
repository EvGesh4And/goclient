package asm250410

import (
	"fmt"
)

type Container struct {
	IO     InputStrategy
	Store  Storage
	UseRaw bool
}

func NewContainer(io InputStrategy, store Storage) *Container {
	return &Container{IO: io, Store: store}
}

func (c *Container) ListItems(factories map[string]func() Student) ([]Student, error) {
	rawItems, err := c.Store.ListRaw()
	if err != nil {
		return nil, err
	}
	out := []Student{}
	for _, e := range rawItems {
		f, ok := factories[e.Class]
		if !ok {
			continue
		}
		obj := f()
		obj.SetData(e.Data)
		out = append(out, obj)
	}
	return out, nil
}

func (c *Container) Add(obj Student) error {
	entry := StoredEntry{Class: obj.TypeName(), Data: obj.GetData()}
	if err := c.Store.AddRaw(entry); err != nil {
		return err
	}
	c.IO.Output("Добавлено: " + obj.String())
	return nil
}

func (c *Container) UpdateByIndex(idx int, obj Student) error {
	entry := StoredEntry{Class: obj.TypeName(), Data: obj.GetData()}
	if err := c.Store.UpdateRaw(idx, entry); err != nil {
		return err
	}
	c.IO.Output("Изменено: " + obj.String())
	return nil
}

func (c *Container) RemoveByIndex(idx int) error {
	_, err := c.Store.RemoveRaw(idx)
	if err != nil {
		return err
	}
	c.IO.Output("Удалено")
	return nil
}

func (c *Container) Clear() error {
	if err := c.Store.Clear(); err != nil {
		return err
	}
	c.IO.Output("Список очищен")
	return nil
}

func (c *Container) SaveToFile(fname string) error {
	if fname == "" {
		c.IO.Output("Пустое имя файла")
		return nil
	}
	if err := c.Store.SaveToFile(fname); err != nil {
		c.IO.Output("Ошибка при сохранении. " + err.Error())
		return err
	}
	c.IO.Output("Сохранено в " + fname)
	return nil
}

func (c *Container) LoadFromFile(fname string, factories map[string]func() Student) error {
	if fname == "" {
		c.IO.Output("Пустое имя файла")
		return nil
	}
	if err := c.Store.LoadFromFile(fname); err != nil {
		c.IO.Output("Ошибка при загрузке. " + err.Error())
		return err
	}
	raw, err := c.Store.ListRaw()
	if err != nil {
		return err
	}
	c.IO.Output(fmt.Sprintf("Загружено %d объектов из %s", len(raw), fname))
	return nil
}
