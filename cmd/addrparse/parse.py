import requests

url = "http://localhost:8080/loc/multimaxmatch"

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python %s <text>" % sys.argv[0])
        sys.exit(1)
    ret = requests.get(url, params={"text": sys.argv[1]})
    print(ret.text)
