import json
import struct
import socket
import time

def send_message_to_control(host, port, msg):

    request_data = bytes(json.dumps(msg), 'utf-8')
    request_data_header = struct.pack('>L', len(request_data))
    raw_request = request_data_header + request_data

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect((host, port))
        s.sendall(raw_request)
        
        raw_response_data_length = s.recv(4)
        response_data_length = struct.unpack('>L', raw_response_data_length)[0]
        raw_response_data = s.recv(response_data_length)
        response = json.loads(raw_response_data.decode('utf-8'))

        return response

def worker(index, host, port):
    print(f'worker {index} launched')
    
    terminate = False
    while not terminate:

        # notify c&c that we exist
        # request a job (starting state) from c&c, start working job
        # periodically send status updates while working, cancel/pause current job if requested
        # send solutions while working
        # send notice of job completion

        time.sleep((index + 1) * 3)

        msg = {
            'msg': f'hello from worker {index}'
        }
        rsp = send_message_to_control(host, port, msg)
        print(f'worker {index} recvd msg from control: {rsp}')
