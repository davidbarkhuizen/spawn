from multiprocessing import Process, Queue
from sserver import listen
import socket
import json
import struct
import time
from worker import worker

# state
# - sequence of moves so far (i.e initial partial solution)
# => current state, current position

# command options
#
# return (all) child states of current state as intermediate states
# run from current state to completion if possible, returning all solutions generated along the way
# halt, returning current intermediate state (if possible ?)

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

        # go through incoming events
        # update internal model
        # decide on next steps
        
        if not q_to_server.empty():

            rq_env = q_to_server.get()
            print(rq_env)

            rq_id = rq_env['id']

            rq = rq_env['rq']

            # determine what immediate response, if any, is appropriate
            # check if a queued response is appropriate/relevant

            rsp_env = {
                'id': rq_id,
                'rsp': f'yo from server to {rq}'
            }
            
            q_from_server.put(rsp_env)

        time.sleep(0.001)

def terminate():

    for wproc in worker_processes:
        wproc.join()

launch('localhost', 8888)