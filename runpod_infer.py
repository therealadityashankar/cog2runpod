import runpod
import os
import time
import requests
import socket
from contextlib import closing
import mimetypes
import tempfile
from runpod.serverless.utils import rp_upload
import base64
import os
   
def check_socket(host, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port)) == 0:
            return True
        else:
            return False

while not check_socket("localhost", 5000):
    time.sleep(1)


def upload_base64(val : str, job):
    print("uploaded_file")
    data_head_start, data = val.split(",", maxsplit=1)
    mimetype = data_head_start.split(";")[0].split(":")[1]
    extension = mimetypes.guess_extension(mimetype)
    data = data.encode("utf-8")
    data = base64.b64decode(data)

    with tempfile.NamedTemporaryFile(suffix=extension) as fp:
        fp.write(data)
        url = rp_upload.upload_file_to_bucket(job['id']+extension, fp.name)

    return url

def upload_if_base64_in_list_or_dict(iterato, job):
    if type(iterato) == dict:
        ret = {}
        for key, val in iterato.items():
            if type(val) == str and val.startswith("data:"):
                x = val[:30].split(",", 1)[0]

                if ";" in x:
                    _type = x.split(";", 1)[1]

                    if _type == "base64":
                        val = upload_base64(val, job)
            else:
                if type(val) == dict or type(val) == list:
                    val = upload_if_base64_in_list_or_dict(val, job)
            
            ret[key] = val

        return ret

    elif type(iterato) == list:
        ret = []

        for val in iterato:
            if type(val) == str and val.startswith("data:"):
                x = val[:30].split(",", 1)[0]

                if ";" in x:
                    _type = x.split(";", 1)[1]

                    if _type == "base64":
                        val = upload_base64(val, job)

            if type(val) == dict or type(val) == list:
                val = upload_if_base64_in_list_or_dict(val, job)
            # replace val produced for upload code to s3 or something
            ret.append(val)

        return ret
    
    return iterato




def handler(event : dict):
    input_details : dict = event['input']
    spec = requests.get("http://localhost:5000/openapi.json").json()

    if 'spec' in input_details:
        output = spec
    else:
        output = requests.post("http://localhost:5000/predictions", json={
            "input" : event['input']
        }).json()

        output = upload_if_base64_in_list_or_dict(output, event)
            

    return {
        "cog_output": output
    }


runpod.serverless.start({
    "handler": handler
})