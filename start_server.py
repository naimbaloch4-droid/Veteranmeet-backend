#!/usr/bin/env python
import os
import sys
import subprocess
import time

def start_server():
    print("Starting VeteranMeet Django API Server...")
    print("Killing any existing Django processes...")
    
    # Kill any existing Django processes
    try:
        subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                      capture_output=True, check=False)
        time.sleep(2)
    except:
        pass
    
    print("Starting fresh Django server...")
    print("Server will be available at: http://127.0.0.1:8000/")
    print("Press Ctrl+C to stop the server\n")
    
    # Start Django server
    subprocess.run([sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000'])

if __name__ == '__main__':
    start_server()