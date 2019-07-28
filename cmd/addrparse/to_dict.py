import gzip
import json

def process(f, ofile):
    if f.endswith(".gz"): fp = gzip.open(f, 'rt')
    else: fp = open(f, 'rt')
    data = {}
    for line in fp:
        item = line.strip().split('\t')
        if len(item) != 2:
            print("err line: %s" % line.strip())
            continue
        for key in item[1].split(','):
            if key not in data: data[key] = {"loc": []}
            data[key]["loc"].append(item[0])
    out = open(ofile, "w")
    max_cnt = 0
    key = ''
    for k, v in data.items():
        one = json.dumps({"k": k, "v": v}, ensure_ascii=False)
        out.write(one+"\n")
        if len(v['loc']) > max_cnt:
            max_cnt = len(v['loc'])
            key = k
    out.close()
    print("%s: %d" % (key, max_cnt))

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python %s <in_file> <out_file>" % sys.argv[0])
        sys.exit(1)
    process(sys.argv[1], sys.argv[2])
