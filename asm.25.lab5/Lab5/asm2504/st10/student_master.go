package asm250410

type StudentMaster struct {
	*StudentBachelor
}

func NewStudentMaster() *StudentMaster {
	base := NewStudentBachelor()
	for i := range base.fields {
		if base.fields[i].Key == "diploma_topic" {
			base.fields[i].Label = "Тема магистерской диссертации"
		}
	}
	base.fields = append(base.fields, FieldDef{"publications", "Научные публикации"}, FieldDef{"internship", "Стажировка"})
	for _, f := range base.fields {
		if _, ok := base.data[f.Key]; !ok {
			base.data[f.Key] = nil
		}
	}
	return &StudentMaster{StudentBachelor: base}
}

func (s *StudentMaster) TypeName() string             { return "Магистр" }
func (s *StudentMaster) Data() map[string]interface{} { return s.data }
func (s *StudentMaster) Fields() []FieldDef           { return s.fields }
func (s *StudentMaster) String() string               { return formatString(s) }
