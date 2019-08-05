import requests
import json
import gzip
from flask import Flask, request, Response
#app = Flask(__name__)
app = Flask(__name__, static_url_path='')

kv = {}

def load_dict():
    global kv
    for line in gzip.open("2018_addr_dict.txt.gz", "rt"):
        item = line.strip().split("\t")
        #kv[item[0]] = item[1].split(",")[0]
        kv[item[0]] = item[1].split(",")

load_dict()

def code2name(code):
    global kv
    if code not in kv: return ''
    return kv[code][0]

url = "http://localhost:8080/loc/multimaxmatch"

keys = ["province","city","county","town","village",]
rkeys = list(reversed(keys))
codelens = {"province":2,"city":4,"county":6,"town":9,"village":12,}

def addr_object(code):
    ret = {}
    l = len(code)
    for key in keys:
        if codelens[key] > l: break
        name = code2name(code[:codelens[key]])
        if name == '':
            break
        ret[key] = name
    return ret

def process(text):
    ret = requests.get(url, params={"text": text})
    item = json.loads(ret.text)
    if item['status'] != 'OK': return item['status']
    msg = item['message']
    addr = []
    for k, v in msg.items():
        for hit in v['hits']:
            addr.append({"value":v['value'], "name":k, "pos":hit})
    addr.sort(key=lambda x:x['pos']['start'])
    num = len(addr)
    result = []
    last_end = 0
    for i in range(num):
        start = addr[i]['pos']['start']
        end = addr[i]['pos']['end']
        for key in keys:
            if key in addr[i]['value']:
                item = {"level": key,
                        "address": [{"code": x} for x in addr[i]['value'][key]],
                        "start": start, "end": end, "text": addr[i]['name'],
                        "length": end-start}
                break
        for j in range(i+1, num):
            end = addr[j]['pos']['end']
            for k in rkeys:
                if codelens[k] <= codelens[key]: continue
                if k not in addr[j]['value']: continue
                v = addr[j]['value'][k]
                #print(key, j, k, v)
                for code in v:
                    ok = False
                    for l in range(i, j):
                        ok = False
                        check_cnt = 0
                        for kk, vv in addr[l]['value'].items():
                            if codelens[kk] >= codelens[k]: continue
                            check_cnt += 1
                            prefix = code[:codelens[kk]]
                            for xcode in vv:
                                if xcode == prefix:
                                    ok = True
                                    break
                            if ok: break
                        if check_cnt == 0: ok = True
                        if not ok: break
                    if ok:
                        txt = text.encode('utf-8')[start:end].decode('utf-8')
                        if item and item['level'] == k:
                            item['address'].append({"code": code})
                        else:
                            item = {"level": k, "address": [{"code": code}],
                                    "start": start, "end": end,
                                    "text": txt, "length": end-start}
                        #key = k
        if item['end'] > last_end:
            last_end = item['end']
            #if type(item['code']) is list: item['addr'] = [addr_object(x) for x in item['code']]
            #else: item['addr'] = addr_object(item['code'])
            for x in item['address']:
                x.update(addr_object(x['code']))
            result.append(item)
    result.sort(key=lambda x:x['length'], reverse=True)
    return result

@app.route("/api")
def get():
    r = request.args.get('text', '')
    if r == "":
        return Response(json.dumps({'status':"error", 'message':"empty input"}))
    result = process(r)
    return Response(json.dumps({'status':"ok", 'message':result}, ensure_ascii=False),
            mimetype="application/json")

@app.route("/code")
def get_code():
    r = request.args.get('code', '')
    if r == "":
        return Response(json.dumps({'status':"error", 'message':"empty input"}))
    global kv
    if r not in kv:
        return Response(json.dumps({'status':"error", 'message':"%s not found" % r}))
    return Response(json.dumps({'status':"ok", 'message':kv[r]}, ensure_ascii=False))

@app.route('/')
def index():
    return app.send_static_file('index.html')#

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)
