from collections import deque
import concurrent.futures
import time
import random

def BFS(tree, start, end):
    paths = []
    queue = deque([(start, [start])])

    while queue:
        node, path = queue.popleft()
        for neighbor in tree[node]:
            if neighbor in path:
                continue
            if neighbor == end:
                paths.append(path + [neighbor])
            else:
                queue.append((neighbor, path + [neighbor]))
    return paths


def BFS_parallel(tree, start, end):
    paths = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for node in tree[start]:
            futures.append(executor.submit(BFS, tree, node, end))

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                for path in result:
                    paths.append([start] + path)
    return paths


graph = {}
nodes = [chr(i) for i in range(65, 91)]
for node in nodes:
    connections = random.sample(nodes, random.randint(2, 5))  
    if node in connections:
        connections.remove(node)  
    graph[node] = connections


start = 'A'
end = 'Z'


print("Caminhos BFS sequencial:")
time_seq_start = time.time()
seq_paths = BFS(graph, start, end)
time_seq_end = time.time()
print(seq_paths)
print(f"Tempo de execução: {time_seq_end - time_seq_start:.6f} segundos")

print()


print("Caminhos BFS paralelo:")
time_par_start = time.time()
par_paths = BFS_parallel(graph, start, end)
time_par_end = time.time()
print(par_paths)
print(f"Tempo de execução: {time_par_end - time_par_start:.6f} segundos")

print()


if (time_par_end - time_par_start) > 0:
    speedup = (time_seq_end - time_seq_start) / (time_par_end - time_par_start)
    print(f"Speedup: {speedup:.6f}x")
else:
    print("Speedup: Infinito (tempo paralelo foi quase zero)")
