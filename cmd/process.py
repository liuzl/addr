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

def city(item): x(item, 'city')
def county(item): x(item, 'county')
def town(item): x(item, 'town')
def village(item): x(item, 'village')

def main(f):
    for line in open(f):
        if line.strip() == "": continue
        item = json.loads(line)
        cls = item['from_parser_']
        if cls == "addr_year": province(item)
        elif cls == "province": city(item)
        elif cls == "city": county(item)
        elif cls == "county": town(item)
        elif cls == "town": village(item)

if __name__ == "__main__":
    main("../20190721000000.dat")
