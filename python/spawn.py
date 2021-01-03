from multiprocessing import Process, Queue
from sserver import listen
import socket
import json
import struct
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

        time.sleep((index + 1) * 3)

        msg = {
            'msg': f'hello from worker {index}'
        }
        rsp = send_message_to_control(host, port, msg)
        print(f'worker {index} recvd msg from control: {msg}')

worker_processes = []

def spawn_workers(count, host, port):

    for z in range(count):
        p = Process(target=worker, args=(z, host, port))
        p.start()
        worker_processes.append(p)

def launch(host, port):

    q_to_server = Queue()
    q_from_server = Queue()

    # launch TCP socket server in own thread

    # launch local machine workers
    worker_count = 2
    spawn_workers(worker_count, host, port)

    p = Process(target=listen, args=(host, port, q_to_server, q_from_server))
    p.start()

    while True:
        
        if not q_to_server.empty():

            rq_env = q_to_server.get()
            print(rq_env)

            rq_id = rq_env['id']

            rq = rq_env['rq']

            rsp_env = {
                'id': rq_id,
                'rsp': f'yo from server to {rq}'
            }
            
            q_from_server.put(rsp_env)

def terminate():

    for wproc in worker_processes:
        wproc.join()

launch('localhost', 8888)