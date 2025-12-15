package asm250410

type Student interface {
	TypeName() string
	Fields() []FieldDef
	GetData() map[string]interface{}
	SetData(map[string]interface{})
	ValidateField(name, raw string) (bool, interface{}, string)
	String() string
}

type FieldDef struct {
	Key   string
	Label string
}
