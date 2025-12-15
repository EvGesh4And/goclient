package akm250118

type EmployeeListResponse struct {
	Employees []map[string]interface{} `json:"employees"`
}

type ClearResponse struct {
	Removed int `json:"removed"`
}
