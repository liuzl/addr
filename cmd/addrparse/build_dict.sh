go get github.com/liuzl/d/cmd/csv2dict

for t in province city county town village;do
    echo $t
    csv2dict -dict_dir dicts -dst loc -src $t.csv -tag $t
done

