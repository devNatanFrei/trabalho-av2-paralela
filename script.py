
from collections import deque
import concurrent.futures


def BSF(tree, start, end):
   visited = []
   queue = deque([start])
   
   while queue:
        node = queue.popleft()
        if node not in visited:
            visited.append(node)
            print(node, end=" ")
            
            for child in tree[node]:
                if child not in visited:
                    queue.append(child)
                    
                
def search_path(neighbor, end, tree):
    return BSF(tree, neighbor, end)


def BSF_paralel(tree, start, end):
    paths = []
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for node in tree[start]:
            futures.append(executor.submit(search_path, tree, node, end))
        
        for future in concurrent.futures.as_completed(futures):
            for path in future.result():
                paths.append([start] + path)
    
    return paths
    
