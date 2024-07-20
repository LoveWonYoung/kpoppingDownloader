package main

import (
	"encoding/json"
	"fmt"
	"io"
	"karina/downloader"
	"net/http"
	"regexp"
	"sync"
)

var wg sync.WaitGroup

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
func gethtmlText(url string) string {
	client := http.Client{}
	req, _ := http.NewRequest("GET", url, nil)
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

// 得到图片的链接，返回的是[]string
func reqList() []string {
	var retImageList []string
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
		retImageList = append(retImageList, "https://kpopping.com"+image[1])
	}
	return retImageList
}

//多线程请求上述列表，先拼接，返回的是每个链接指向的所有图片链接

// https://kpopping.com/profiles/idol/Karina2/latest-pictures

// 从返回的链接中找到所有图片链接

func getOnePicLink(pImageLink []string) []string {
	// fmt.Println(pImageLink)
	//次数实现多线程请求12个链接
	var opl []string

	// 请求一次
	for _, req := range pImageLink {
		wg.Add(1)
		re := regexp.MustCompile(`<a href="/documents/(.*?)" data`)

		go func(link string) {
			onePicLink := re.FindAllStringSubmatch(link, -1)
			for _, pL := range onePicLink {
				fmt.Println(pL[1])
				//imageName := strings.Split(strings.Split(pL[1], "/")[3], ".")[0]
				opl = append(opl, "https://kpopping.com/documents/"+pL[1])

			}
			wg.Done()
		}(req)
	}
	fmt.Println(opl)
	wg.Wait()
	return opl
}

func threadDonwload(t []string) {
	fmt.Println(t)
	for _, j := range t {
		wg.Add(1)
		go func(n string) {
			fmt.Println(n) //此处实现下载

			wg.Done()
		}(j)
	}
	wg.Wait()
}
func main() {

	//reqList()
	//threadDonwload(getOnePicLink(reqList()))
	downloader.OnePicDownload("a")
}
