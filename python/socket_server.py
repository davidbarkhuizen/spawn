from multiprocessing import Process
import socket
import struct
import json
import time
import os

def new_connection(conn, addr, q_to_server, q_from_server):
    
    with conn:

        raw_rq_data_length = conn.recv(4)
        rq_data_length = struct.unpack('>L', raw_rq_data_length)[0]
        raw_rq_data = conn.recv(rq_data_length)
        rq = json.loads(raw_rq_data.decode('utf-8'))

        rq_id = os.urandom(16).hex()

        envelope = {
            'id': rq_id,
            'rq': rq
        }

        q_to_server.put(envelope)
        
        rsp_o = None
        while True:
            if not q_from_server.empty():        
                rsp_envelope = q_from_server.get() # TODO timeout
                
                # not for us, put it back so others can get to it
                if rsp_envelope['id'] != rq_id:
                    q_from_server.put(rsp_envelope)
                    time.sleep(0.1)
                    continue                                
                else:
                    rsp_o = rsp_envelope['rsp']
                    break
                    
        rsp_data = bytes(json.dumps(rsp_o), 'utf-8')
        
        rsp_data_header = struct.pack('>L', len(rsp_data))
        raw_rsp = rsp_data_header + rsp_data

        conn.sendall(raw_rsp)

def listen(host, port, q_to_server, q_from_server):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        s.bind((host, port))
        s.listen()
        while True:
            conn, addr = s.accept()
            p = Process(target=new_connection, args=(conn, addr, q_to_server, q_from_server))
            p.start()