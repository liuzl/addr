package main

import (
	"encoding/json"
	"flag"
	"time"

	"crawler.club/et"
	"github.com/golang/glog"
	"zliu.org/filestore"
)

var (
	start = flag.String("start", "addr", "the parser name for the start url")
	dir   = flag.String("dir", "data", "the data dir")
	sleep = flag.Int("sleep", -1, "in seconds")
)

func main() {
	flag.Parse()
	defer glog.Flush()

	fs, err := filestore.NewFileStore(*dir)
	if err != nil {
		glog.Fatal(err)
	}
	defer fs.Close()
	p, err := pool.GetParser(*start, false)
	if err != nil {
		glog.Fatal(err)
	}

	glog.Infof("start crawling from %s", p.ExampleUrl)

	var tasks = []*et.UrlTask{&et.UrlTask{ParserName: *start, Url: p.ExampleUrl}}
	for {
		if len(tasks) == 0 {
			break
		}
		task := tasks[0]
		tasks = tasks[1:]
		glog.Info(task.Url)
		new_tasks, items, err := ParseTask(task)
		if err != nil {
			glog.Error(err)
			continue
		}
		tasks = append(tasks, new_tasks...)
		for _, item := range items {
			b, _ := json.Marshal(item)
			fs.WriteLine(b)
		}
		if *sleep > 0 {
			time.Sleep(time.Duration(*sleep) * time.Second)
		}
	}
}
