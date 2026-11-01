"""One request per debug connection; append local QA receipts."""
import socket,json,sys
from pathlib import Path
request=json.loads(sys.argv[1]);request.setdefault("id",1)
with socket.create_connection(("127.0.0.1",int(sys.argv[2]) if len(sys.argv)>2 else 4370),timeout=4) as s:
 s.settimeout(8);s.sendall((json.dumps(request)+chr(10)).encode());r=b""
 while bytes([10]) not in r:
  b=s.recv(262144)
  if not b:break
  r+=b
result=json.loads(r)
with open("puzzle-qa.jsonl","a") as f:f.write(json.dumps({"request":request,"response":result})+chr(10))
print(json.dumps(result))

if not result.get("ok"):
 raise SystemExit(1)
