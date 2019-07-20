package main

import (
	"fmt"
	"log"

	"zliu.org/goutil"
)

func main() {
	p, err := pool.GetParser("addr", false)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(p.ExampleUrl)
	tasks, _, err := Parse("addr", p.ExampleUrl)
	if err != nil {
		log.Fatal(err)
	}
	for _, task := range tasks {
		fmt.Println(task.Url)
		ret, _ := goutil.RegexpParse(task.Url, `\d+`)
		if len(ret) != 1 {
			log.Fatal(task.Url, " error")
		}
		year := ret[0]
		fmt.Println(year)
	}
}
