import requests
import json
import gzip

url = "http://localhost:8080/loc/multimaxmatch"
code_url = "http://127.0.0.1:5000/?code=%s"

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
    addr = {}
    for k, v in msg.items():
        #print(k, v)
        for addr_type, value in v['value'].items():
            if addr_type not in addr:
                addr[addr_type] = []
            addr[addr_type].append({"code":value, "name":k, "pos":v['hits']})
    print(addr)
    if "province" in addr:
        text = code2name(addr['province'][0]['code'][0])
        print(text)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python %s <text>" % sys.argv[0])
        sys.exit(1)
    ret = process(sys.argv[1])
    print(ret)
