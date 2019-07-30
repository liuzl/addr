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
    '''
    if "province" in addr:
        text = code2name(addr['province'][0]['code'][0])
        print(text)
    '''
    result = []
    '''
    for key in rkeys:
        if addr[key]: break
    '''
    for key in rkeys:
        for x in addr[key]:
            for code in x['code']:
                if check(code, key, addr):
                    result.append((key,code))
    print(result)

def check(code, key, addr):
    for k in keys:
        if k == key: break
        if len(addr[k]) == 0: continue

        # 每个层级都需要对应
        ok = False
        prefix = code[:codelens[k]]
        for x in addr[k]:
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
    ret = process(sys.argv[1])
    print(ret)
