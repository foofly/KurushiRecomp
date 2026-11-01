"""Queue an explicit JSON route, with receipts recorded by qa_client."""
import json,subprocess,sys
steps=json.loads(sys.argv[1]);at=int(sys.argv[2]) if len(sys.argv)>2 else 0
commands=[dict(cmd="input_route_clear")]+[dict(cmd="input_route_append",buttons=b,frames=f) for b,f in steps]+[dict(cmd="input_route_start",at_frame=at)]
for command in commands:
 subprocess.run([sys.executable,"tools/qa_client.py",json.dumps(command)],check=True)
