package asm250410

type InputStrategy interface {
	Output(msg string)
	InputRaw(prompt string) string
	SelectType(factories []func() Student) int
	InputFields(obj Student) map[string]string
	SelectIndex(items []Student) int
	InputUpdates(obj Student) map[string]string
}
