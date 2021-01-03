from multiprocessing import Process
import socket
import struct
import json

def new_connection(conn, addr):
    
    with conn:
        print('Connected by', addr)

        raw_rq_data_length = conn.recv(4)
        rq_data_length = struct.unpack('>L', raw_rq_data_length)[0]
        raw_rq_data = conn.recv(rq_data_length)
        rq = json.loads(raw_rq_data.decode('utf-8'))

        print(f'recvd from worker: {rq}')

        rsp_o = { 'fish': 'cat' }
        rsp_data = bytes(json.dumps(rsp_o), 'utf-8')
        
        rsp_data_header = struct.pack('>L', len(rsp_data))
        raw_rsp = rsp_data_header + rsp_data

        conn.sendall(raw_rsp)

        # done, terminate - context manager will close conn

def listen(host, port):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        s.bind((host, port))
        s.listen()
        while True:
            conn, addr = s.accept()
            p = Process(target=new_connection, args=(conn, addr))
            p.start()