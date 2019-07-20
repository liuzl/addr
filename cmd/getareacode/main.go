package main

import (
	"fmt"

	"github.com/golang/glog"
	"zliu.org/goutil"
)

func main() {
	p, err := pool.GetParser("addr", false)
	if err != nil {
		glog.Fatal(err)
	}
	fmt.Println(p.ExampleUrl)
	years, _, err := Parse("addr", p.ExampleUrl)
	if err != nil {
		glog.Fatal(err)
	}
	for _, task := range years {
		fmt.Println(task.Url)
		ret, _ := goutil.RegexpParse(task.Url, `\d+`)
		if len(ret) != 1 {
			glog.Fatal(task.Url, " error")
		}
		year := ret[0]
		fmt.Println(year)
		tasks, items, err := Parse(task.ParserName, task.Url)
		fmt.Println(items, tasks, err)
	}
}
