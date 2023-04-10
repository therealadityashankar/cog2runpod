import runpod
import os
import time
import requests
import socket
from contextlib import closing
   
def check_socket(host, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port)) == 0:
            return True
        else:
            return False

while not check_socket("localhost", 5000):
    time.sleep(1)

def handler(event):
    output = requests.post("http://localhost:5000/predictions", json={
        "input" : event['input']
    }).json()
        
    return output


runpod.serverless.start({
    "handler": handler
})