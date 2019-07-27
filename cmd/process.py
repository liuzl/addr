import json

def province(item):
    for p in item['province']:
        pos = p['province'].rfind('/') + 1
        print("%s\t%s\t%s" % ('province',
            p['province'][pos:].replace('.html','')+('0'*10),
            p['name']))

def x(item, name):
    if type(item[name]) is list:
        for c in item[name]:
            print("%s\t%s\t%s" % (name, c['code'], c['name']))
    else:
        print("%s\t%s\t%s" % (name, item[name]['code'], item[name]['name']))

def main(f):
    for line in open(f):
        if line.strip() == "": continue
        item = json.loads(line)
        cls = item['from_parser_']
        if cls == "addr_year": province(item)
        elif cls == "province": x(item, 'city')
        elif cls == "city": x(item, 'county')
        elif cls == "county": x(item, 'town')
        elif cls == "town": x(item, 'village')

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: %s <file>" % sys.argv[0])
        sys.exit(0)
    main(sys.argv[1])
