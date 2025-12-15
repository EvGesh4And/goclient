package asm250410

type StudentGraduate struct {
	*StudentMaster
}

func NewStudentGraduate() *StudentGraduate {
	master := NewStudentMaster()
	for i := range master.fields {
		if master.fields[i].Key == "diploma_topic" {
			master.fields[i].Label = "Тема кандидатской диссертации"
		}
	}
	master.fields = append(master.fields, FieldDef{"publications", "Научные публикации"})
	for _, f := range master.fields {
		if _, ok := master.data[f.Key]; !ok {
			master.data[f.Key] = nil
		}
	}
	return &StudentGraduate{StudentMaster: master}
}

func (s *StudentGraduate) TypeName() string             { return "Аспирант" }
func (s *StudentGraduate) Data() map[string]interface{} { return s.data }
func (s *StudentGraduate) Fields() []FieldDef           { return s.fields }
func (s *StudentGraduate) String() string               { return formatString(s) }
