import gzip
import json
from flask import Flask, request, Response
app = Flask(__name__)

kv = {}

def load_dict():
    global kv
    for line in gzip.open("2018_addr_dict.txt.gz", "rt"):
        item = line.strip().split("\t")
        kv[item[0]] = item[1].split(",")[0]

load_dict()

@app.route("/")
def get():
    r = request.args.get('code', '')
    if r == "":
        return Response(json.dumps({'status':"error", 'message':"empty input"}))
    global kv
    if r not in kv:
        return Response(json.dumps({'status':"error", 'message':"%s not found" % r}))
    return Response(json.dumps({'status':"ok", 'message':kv[r]}))

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
