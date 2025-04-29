from collections import deque
from multiprocessing import Process, Queue
import time
import random
import string
import pprint

def BFS(tree, initial, final):
    queue = deque([(initial, [initial])])
    paths = []

    while queue:
        current_node, path = queue.popleft()
        for neighbor in tree.get(current_node, []):
            if neighbor in path:
                continue
            if neighbor == final:
                paths.append(path + [neighbor])
            else:
                queue.append((neighbor, path + [neighbor]))
    return paths


def worker(tree, neighbor, final, queue_results):
    result = BFS(tree, neighbor, final)
    queue_results.put((neighbor, result))

def BFS_parallel(tree, initial, final):
    processes = []
    queue_results = Queue()
    finded_paths = []

    for neighbor in tree.get(initial, []):
        p = Process(target=worker, args=(tree, neighbor, final, queue_results))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    while not queue_results.empty():
        neighbor, result = queue_results.get()
        for path in result:
            finded_paths.append([initial] + path)
    return finded_paths

def generate_graph():
    graph = {}
    nodes = [chr(i) for i in range(65, 75)]  
    for node in nodes:
        connections = random.sample(nodes, random.randint(1, 3))
        if node in connections:
            connections.remove(node)
        graph[node] = connections
    return graph

if __name__ == "__main__":
    initial = 'A'
    final = 'J'

    graph = generate_graph()

    print("Grafo gerado:")
    pprint.pprint(graph)

    print("\nCaminhos BFS sequencial:")
    time_seq_start = time.time()
    seq_paths = BFS(graph, initial, final)
    time_seq_end = time.time()
    print(seq_paths)
    print(f"Tempo de execução: {time_seq_end - time_seq_start:.6f} segundos")

    print("\nCaminhos BFS paralelo:")
    time_par_start = time.time()
    par_paths = BFS_parallel(graph, initial, final)
    time_par_end = time.time()
    print(par_paths)
    print(f"Tempo de execução: {time_par_end - time_par_start:.6f} segundos")

    if (time_par_end - time_par_start) > 0:
        speedup = (time_seq_end - time_seq_start) / (time_par_end - time_par_start)
        print(f"\nSpeedup: {speedup:.6f}x")
