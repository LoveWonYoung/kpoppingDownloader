package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"regexp"
)

type urlJson struct {
	Items        map[string]string `json:"items"`
	Max          int               `json:"max"`
	AppendTarget string            `json:"appendTarget"`
	Content      string            `json:"content"`
	ReplaceHTML  string            `json:"replaceHtml"`
}

func htmlText(url string) string {
	client := http.Client{}
	req, _ := http.NewRequest("POST", url, nil)
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer func(Body io.ReadCloser) {
		err := Body.Close()
		if err != nil {
			fmt.Println(err)
		}
	}(resp.Body)

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		panic(err)
	}
	// fmt.Println(string(body))
	return string(body)
}
func reqList() {
	c := htmlText("https://kpopping.com/profiles/idol/Wonyoung/latest-pictures/1")
	var html urlJson
	err := json.Unmarshal([]byte(c), &html)
	if err != nil {
		fmt.Println(err)
	}
	//fmt.Println(html.Content)

	// 定义一个正则表达式
	re := regexp.MustCompile(`<a href="(.*?)" class="cell" aria-label="album">`)
	imageList := re.FindAllStringSubmatch(html.Content, -1)
	for _, image := range imageList {
		fmt.Println(image[1])
	}
}

// https://kpopping.com/profiles/idol/Karina2/latest-pictures
func main() {
	reqList()
}
