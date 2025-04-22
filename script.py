
from collections import deque
import concurrent.futures






def BSF(tree, target):
   visited = []
   queue = deque([target])
   
   while queue:
        node = queue.popleft()
        if node not in visited:
            visited.append(node)
            print(node, end=" ")
            
            for child in tree[node]:
                if child not in visited:
                    queue.append(child)
                    