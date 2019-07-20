package main

import (
	"fmt"
	"log"

	"crawler.club/dl"
)

func main() {
	p, err := pool.GetParser("addr", false)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(p.ExampleUrl)
	ret := dl.DownloadUrl(p.ExampleUrl)
	fmt.Println(ret.StatusCode)
}
