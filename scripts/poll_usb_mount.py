import time
import subprocess
import sys
import json

print("🔍 Waiting for Xteink X4 USB Mass Storage mode...")

for i in range(30):
    res = subprocess.run(["lsblk", "-J"], capture_output=True, text=True)
    if res.returncode == 0 and "sd" in res.stdout:
        try:
            data = json.loads(res.stdout)
            for dev in data.get("blockdevices", []):
                if dev["name"].startswith("sd"):
                    children = dev.get("children", [])
                    target_part = f"/dev/{children[0]['name']}" if children else f"/dev/{dev['name']}"
                    print(f"⚡ Detected USB drive: {target_part}")
                    
                    mount_res = subprocess.run(["sudo", "mount", target_part, "/mnt/x4"], capture_output=True, text=True)
                    if mount_res.returncode == 0:
                        print(f"✅ SUCCESSFULLY MOUNTED {target_part} to /mnt/x4")
                        sys.exit(0)
                    else:
                        # Try mounting via UDisks2 or gio
                        gio_res = subprocess.run(["udisksctl", "mount", "-b", target_part], capture_output=True, text=True)
                        print(f"UDisks2 mount output: {gio_res.stdout} {gio_res.stderr}")
                        sys.exit(0)
        except Exception as e:
            print(f"Parse error: {e}")
    time.sleep(2)

print("⏳ Timeout waiting for USB Mass Storage mode. Please toggle USB Storage on the X4 screen.")
