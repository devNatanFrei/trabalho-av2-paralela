from collections import deque
import concurrent.futures
import time
import random

def BFS(matrix, start, target):
    paths = []
    queue = deque([(start, [start])])

    rows, cols = len(matrix), len(matrix[0])

    while queue:
        (x, y), path = queue.popleft()
        
        if matrix[x][y] == target:
            paths.append(path)
            continue
        
        # Movimentos: cima, baixo, esquerda, direita
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in path:
                queue.append(((nx, ny), path + [(nx, ny)]))
                
    return paths

def BFS_parallel(matrix, target):
    paths = []
    rows, cols = len(matrix), len(matrix[0])
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i in range(rows):
            for j in range(cols):
                futures.append(executor.submit(BFS, matrix, (i, j), target))
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                paths.extend(result)
    
    return paths

# Criando uma matriz aleatória
random.seed(42)
matrix = [[random.randint(1, 9) for _ in range(5)] for _ in range(5)]

target = 5

print("Matriz:")
for row in matrix:
    print(row)

print(f"\nBuscando o número: {target}")

print("\nCaminhos BFS sequencial:")
time_seq_start = time.time()
seq_paths = []
for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        seq_paths.extend(BFS(matrix, (i, j), target))
time_seq_end = time.time()
print(seq_paths)
print(f"Tempo de execução: {time_seq_end - time_seq_start:.6f} segundos")

print("\nCaminhos BFS paralelo:")
time_par_start = time.time()
par_paths = BFS_parallel(matrix, target)
time_par_end = time.time()
print(par_paths)
print(f"Tempo de execução: {time_par_end - time_par_start:.6f} segundos")

print()
if (time_par_end - time_par_start) > 0:
    speedup = (time_seq_end - time_seq_start) / (time_par_end - time_par_start)
    print(f"Speedup: {speedup:.6f}x")
else:
    print("Speedup: Infinito (tempo paralelo foi quase zero)")
