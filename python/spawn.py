from multiprocessing import Process

def log(s):
    print(s)

def worker(index, host, port):
    log(f'worker {index} launched')
    
    terminate = False
    while not terminate:
        pass

worker_processes = []

def spawn_workers(count, host, port):

    for z in range(count):
        p = Process(target=worker, args=(z, host, port))
        p.start()
        worker_processes.append(p)

def launch(host, port):

    # launch TCP socket server in own thread

    # launch local machine workers
    worker_count = 2
    spawn_workers(worker_count, host, port)

    while True:
        pass

def terminate():

    for wproc in worker_processes:
        wproc.join()

launch('localhost', 8888)