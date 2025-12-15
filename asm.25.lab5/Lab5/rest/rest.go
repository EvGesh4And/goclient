package rest

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

func DoRequest(method string, st string, cmd string, data any) io.ReadCloser {

	url := "http://127.0.0.1:5000/" + st + "api/"
	var jdata []byte
	var pdata io.Reader

	fmt.Println(url)

	if data != nil {
		jdata, _ = json.Marshal(data)
		pdata = bytes.NewReader(jdata)
	}

	req, err := http.NewRequest(method, url+cmd, pdata)
	if err != nil {
		fmt.Printf("Request error: %s\n", err)
	}
	if jdata != nil {
		req.Header.Set("Content-Type", "application/json")
	}

	res, err := http.DefaultClient.Do(req)
	if err != nil {
		fmt.Printf(method+" error: %s\n", err)
	}

	if res.ContentLength != 0 {
		return res.Body
	}

	res.Body.Close()

	return nil
}

func GetDecoded(body io.ReadCloser, result any) bool {
	if body != nil {
		json.NewDecoder(body).Decode(&result)
		body.Close()
		return true
	}
	return false
}

func GetAny(body io.ReadCloser) any {
	var result any
	if GetDecoded(body, &result) {
		return result
	}
	return nil
}

func GetAnyDirect(body io.ReadCloser) any {
	if body != nil {
		defer body.Close()
		var result any
		json.NewDecoder(body).Decode(&result)
		return result
	}
	return nil
}

func GetBytes(body io.ReadCloser) []byte {
	if body != nil {
		defer body.Close()
		resBody, _ := io.ReadAll(body)
		return resBody
	}
	return nil
}
