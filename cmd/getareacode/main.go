package main

import (
	"flag"
	"fmt"

	"github.com/golang/glog"
	"zliu.org/goutil"
)

var (
	start = flag.String("start", "addr", "the parser name for the start url")
)

func main() {
	flag.Parse()
	defer glog.Flush()

	p, err := pool.GetParser(*start, false)
	if err != nil {
		glog.Fatal(err)
	}
	fmt.Println(p.ExampleUrl)
	years, _, err := Parse(*start, p.ExampleUrl)
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
