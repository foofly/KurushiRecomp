"""Run a short frame-counted input route and capture its resulting state."""
import json,subprocess,sys,time
from pathlib import Path
steps=json.loads(sys.argv[1]);name=sys.argv[2]
def request(cmd,**kwargs):
 r=subprocess.run([sys.executable,"tools/qa_client.py",json.dumps(dict(cmd=cmd,**kwargs))],capture_output=True,text=True,check=True)
 return json.loads(r.stdout)
Path(name+"-route.json").write_text(json.dumps(steps,indent=2)+chr(10))
request("input_route_clear")
for buttons,frames in steps:request("input_route_append",buttons=buttons,frames=frames)
request("input_route_start")
end=time.monotonic()+15
while request("input_route_status")["active"]:
 if time.monotonic()>end:raise TimeoutError("route exceeded 15 seconds")
 time.sleep(0.1)
state=request("get_registers");print(json.dumps(state))
print(json.dumps(request("screenshot",path=str(Path(name+".png").resolve()))))
