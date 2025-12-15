package akm250118

type ItemsResponse struct {
	Items []map[string]interface{} `json:"items"`
}

type AddResponse struct {
	ID      int    `json:"id"`
	Message string `json:"message"`
}

type UpdateResponse struct {
	Message string `json:"message"`
}

type DeleteResponse struct {
	Message string `json:"message"`
}

