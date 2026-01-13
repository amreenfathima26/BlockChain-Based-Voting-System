
import os
import sys
import threading
import time
from django.core.management import execute_from_command_line
from pyngrok import ngrok

def run_server():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secure_vote.settings')
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])

import socket

def get_local_ip():
    try:
        # Connect to an external server (doesn't send data) to get the interface IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def start_ngrok():
    # Wait a bit for the server to start
    time.sleep(3)
    
    local_ip = get_local_ip()
    
    try:
        # Open a HTTP tunnel on the default port 8000
        public_url = ngrok.connect(8000).public_url
    except Exception as e:
        print(f"Error connecting: {e}")
        print("Cleaning up existing ngrok process...")
        ngrok.kill()
        print("Waiting 5 seconds for cleanup...")
        time.sleep(5)
        print("Retrying connection...")
        try:
            public_url = ngrok.connect(8000).public_url
        except Exception as e2:
            print(f"Retry failed: {e2}")
            return

    print("\n" + "="*60)
    print(f"1. PUBLIC INTERNET ACCESS:")
    print(f"   {public_url}")
    print(f"   (Use this if you are on a different network/mobile data)")
    print("-" * 60)
    print(f"2. LOCAL NETWORK ACCESS (Same Wi-Fi):")
    print(f"   http://{local_ip}:8000")
    print(f"   (Faster, but requires device to be on same Wi-Fi)")
    print("="*60 + "\n")

if __name__ == '__main__':
    # Start ngrok in a separate thread
    threading.Thread(target=start_ngrok, daemon=True).start()
    
    # Run the server in the main thread
    run_server()
