import json
import struct
import socket
import time

from enum import Enum

WorkerState = Enum('WorkerState', 
    'Idle Busy Paused'
)

ControlCommand = Enum('ControlCommand',
    'Solve Iterate Pause Cancel'
)

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

def iterate(initial_state, initial_partial_solution):
    
    # from initial state
    # work out first child states
    # create node corresponding to initial state
    # create child nodes for each child state

    # if we are set to return only child states
    # then return (them) at this point

    # otherwise, start depth-first search

    new_solutions = []
    interim_states = []

    return new_solutions, interim_states

def worker(index, host, port, message_interval_ms):
    print(f'worker {index} launched')
    
    workerState = WorkerState.Idle

    def handle_control_message(control_message):

        if 


        pass

    terminate = False
    while not terminate:

        status_msg = {
            'id': index,
            'workerState': workerState,
            'new_solutions': [],
            'interim_states': []
        }

        if workerState in [WorkerState.Idle, WorkerState.Paused]:
            time.sleep(message_interval_ms)
        elif workerState == WorkerState.Busy:
            initial_state = None
            initial_partial_solution = None
            new_solutions, interim_states = iterate(initial_state, initial_partial_solution)
            
            status_msg['new_solutions'].extend(new_solutions)
            status_msg['interim_states'].extend(interim_states)

        control_msg = send_message_to_control(host, port, status_msg)
        handle_control_message(control_msg)