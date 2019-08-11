import re
import json

pattern = re.compile(r'\d+号楼\d+单元\d+|\d+\-\d+\-\d+')

def extract(line):
    ret = pattern.findall(line)
    return ret

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python %s <line>" % sys.argv[0])
        sys.exit(1)
    ret = extract(sys.argv[1])
    print(json.dumps(ret, ensure_ascii=False))
