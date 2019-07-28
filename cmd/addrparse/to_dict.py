import gzip
import json

codelen = {2:"province", 4:"city", 6:"county", 9:"town", 12:"village"}

def process(infile):
    if infile.endswith(".gz"): fp = gzip.open(infile, 'rt')
    else: fp = open(infile, 'rt')
    out = {}
    for line in fp:
        item = line.strip().split('\t')
        if len(item) != 2:
            print("err line: %s" % line.strip())
            continue
        f = "%s.csv" % codelen[len(item[0])]
        if f not in out: out[f] = open(f, "w")
        for key in item[1].split(','):
            key = key.strip()
            if key == "": continue
            out[f].write("%s,%s\n" % (key, item[0]))
    for k, v in out.items():
        v.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python %s <in_file>" % sys.argv[0])
        sys.exit(1)
    process(sys.argv[1])
