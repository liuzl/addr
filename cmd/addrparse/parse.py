import requests
import json
import gzip

url = "http://localhost:8080/loc/multimaxmatch"
code_url = "http://127.0.0.1:5000/?code=%s"

keys = ["province","city","county","town","village",]
rkeys = list(reversed(keys))
codelens = {"province":2,"city":4,"county":6,"town":9,"village":12,}

def code2name(code):
    text = requests.get(code_url % code).text
    item = json.loads(text)
    if item['status'] == 'ok': return item['message']
    return ''

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
                            if item['end'] < end: break
                            item['address'].append({"code": code})
                        else:
                            item = {"level": k, "address": [{"code": code}],
                                    "start": start, "end": end,
                                    "text": txt, "length": end-start}
                        #key = k
        if item['end'] > last_end:
            last_end = item['end']
            for x in item['address']:
                x.update(addr_object(x['code']))
            result.append(item)
    result.sort(key=lambda x:x['length'], reverse=True)
    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python %s <text>" % sys.argv[0])
        sys.exit(1)
    ret = process(sys.argv[1])
    for item in ret:
        print(json.dumps(item, ensure_ascii=False))
