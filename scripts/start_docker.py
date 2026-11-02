"""
start_docker.py — Launch Docker Desktop and wait for the daemon to become ready.
"""
import subprocess
import time
import os

DOCKER_EXE = r"C:\Users\gnavy\AppData\Local\Programs\DockerDesktop\Docker Desktop.exe"

print(f"Starting Docker Desktop from {DOCKER_EXE}...")
try:
    subprocess.Popen([DOCKER_EXE])
    print("Docker Desktop process initiated.")
except Exception as e:
    print(f"Failed to start Docker Desktop: {e}")
    exit(1)

print("Polling for Docker daemon readiness (up to 60s)...")
ready = False
for attempt in range(1, 31):
    time.sleep(2)
    res = subprocess.run(["docker", "version", "--format", "{{.Server.Version}}"], capture_output=True, text=True)
    if res.returncode == 0 and res.stdout.strip():
        print(f"\n[PASS] Docker daemon is READY! Version: {res.stdout.strip()}")
        ready = True
        break
    print(f"Waiting... (attempt {attempt}/30)")

if not ready:
    print("\n[WARN] Docker daemon did not respond within 60s.")
    exit(1)

