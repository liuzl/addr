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

def process(text):
    ret = requests.get(url, params={"text": text})
    item = json.loads(ret.text)
    if item['status'] != 'OK': return item['status']
    msg = item['message']
    addr = {key:[] for key in keys}
    for k, v in msg.items():
        for key, value in v['value'].items():
            for hit in v['hits']:
                addr[key].append({"code":value, "name":k, "pos":hit})
    for k, v in addr.items():
        print(k, v)
    result = []
    for key in rkeys:
        for x in addr[key]:
            for code in x['code']:
                if check(code,x['pos'], key, addr):
                    result.append((key,code))
    print(result)

def process2(text):
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
    for i in range(num):
        start = addr[i]['pos']['start']
        end = addr[i]['pos']['end']
        for key in keys:
            if key in addr[i]['value']:
                item = (addr[i]['name'], addr[i]['value'][key], key, start, end)
                break
        for j in range(i+1, num):
            end = addr[j]['pos']['end']
            for k, v in addr[j]['value'].items():
                if codelens[k] <= codelens[key]: continue
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
                        item = (k, code, start, end, txt)
        result.append(item)
    return result

def check(code, pos, key, addr):
    for k in keys:
        if k == key: break
        cnt = 0
        for x in addr[k]:
            if pos != x['pos']: cnt += 1
        if cnt == 0: continue

        # 每个层级都需要对应
        ok = False
        prefix = code[:codelens[k]]
        for x in addr[k]:
            if pos == x['pos']: continue
            for c in x['code']:
                if prefix == c:
                    ok = True
                    break
            if ok: break
        if not ok: return False
    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python %s <text>" % sys.argv[0])
        sys.exit(1)
    ret = process2(sys.argv[1])
    print(ret)
