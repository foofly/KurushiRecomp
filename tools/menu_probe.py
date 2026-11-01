"""Bounded local boot/input smoke probe; outputs private screenshots/logs."""
import json, os, socket, subprocess, time
from pathlib import Path
root = Path(__file__).resolve().parent.parent
os.chdir(root)
def request(cmd, **args):
    with socket.create_connection(("127.0.0.1", 4370), timeout=3) as sock:
        sock.settimeout(5)
        sock.sendall((json.dumps(dict(id=1, cmd=cmd, **args))+chr(10)).encode())
        data = b""
        while bytes([10]) not in data:
            chunk = sock.recv(262144)
            if not chunk: break
            data += chunk
        result = json.loads(data)
        with open("menu-probe.jsonl", "a") as out: out.write(json.dumps(dict(command=cmd, **result))+chr(10))
        return result
def shot(name):
    request("get_registers")
    request("screenshot", path=str(root/(name+".png")))
def press(button):
    request("set_input", buttons=button)
    time.sleep(0.25)
    request("clear_input")
with open("menu-probe.log", "w") as log:
    env=dict(os.environ, PSX_INTERNAL_RESOLUTION="1x", PSX_SUPERSAMPLE="1", PSX_HLE_SCHEDULER="0")
    proc=subprocess.Popen(["./build-release/Kurushi_Recompiled", "--no-launcher", "--renderer", "software"], env=env, stdout=log, stderr=log)
    try:
        time.sleep(75)
        shot("main-menu")
        press("FFDF")
        time.sleep(0.5)
        shot("menu-right")
        press("FF7F")
        press("BFFF")
        time.sleep(8)
        shot("one-player")
        press("BFFF")
        time.sleep(8)
        shot("puzzle-before")
        press("BFFF")
        time.sleep(5)
        shot("puzzle-ready")
        request("set_input", buttons="FFDF")
        time.sleep(1)
        request("clear_input")
        shot("puzzle-after-right")
        request("audio_stats")
    finally:
        proc.kill()
        proc.wait()
