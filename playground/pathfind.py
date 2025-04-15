import heapq
import random

class MapPath:
    def __init__(self, rows, cols, density=0.1, slow=False):
        self.rows = rows
        self.cols = cols
        self.slow = slow
        self.legend = {"empty": 0, "obstacle": 1, "candidate": 2, "path": 3, "target": 4, "slow": 5}
        self.map = self.generate_map(rows, cols, density, slow)

    def generate_map(self, rows, cols, density, slow):
        grid = [[0 for _ in range(cols)] for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                if random.random() < density:
                    grid[i][j] = random.choice([self.legend["obstacle"], self.legend["slow"]] if slow else [self.legend["obstacle"]])
        grid[0][0] = self.legend["empty"]
        grid[rows - 1][cols - 1] = self.legend["empty"]
        return grid

    def distance(self, current, target):
        return ((target[0] - current[0])**2 + (target[1] - current[1])**2)**0.5

    def route(self, start, target, method):
        rows, cols = self.rows, self.cols
        map_data = [row[:] for row in self.map]   
        seen = set([start])
        parent = {}
        cx, cy = start
        map_data[target[0]][target[1]] = self.legend["target"]
        steps = []

         
        if method == "A*":
            self.astar(start, target, map_data, seen, parent, steps, cx, cy)
        elif method == "BFS":
            self.bfs(start, target, map_data, seen, parent, steps, cx, cy)
        elif method == "DFS":
            self.dfs(start, target, map_data, seen, parent, steps, cx, cy)
        elif method == "Dijkstra":
            self.dijkstra(start, target, map_data, seen, parent, steps, cx, cy)
        else:
            raise ValueError(f"Unsupported method: {method}")

         
        path = []
        current = target
        while current in parent:
            path.append(current)
            current = parent[current]
        path.append(start)

         
        for px, py in path:
            map_data[px][py] = self.legend["path"]

         
        steps.append(map_data)  
        return steps

    def dijkstra(self, start, target, map_data, seen, parent, steps, cx, cy):
        queue = [(0, cx, cy)]
        while queue:
            dist, cx, cy = heapq.heappop(queue)
            if (cx, cy) == target:
                map_data[cx][cy] = self.legend["path"]
                break
            map_data[cx][cy] = self.legend["candidate"]
            seen.add((cx, cy))    
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                tx, ty = cx + dx, cy + dy
                if 0 <= tx < self.rows and 0 <= ty < self.cols and (tx, ty) not in seen and map_data[tx][ty] != self.legend["obstacle"]:
                    current = (tx, ty)
                    seen.add(current)
                    parent[current] = (cx, cy)
                    queue.append((self.distance(current, target), tx, ty))
            
            
            steps.append([row[:] for row in map_data])
    def astar(self, start, target, map_data, seen, parent, steps, cx, cy):
        heap = [(0, cx, cy)]
        while heap:
            dist, cx, cy = heapq.heappop(heap)
            if (cx, cy) == target:
                map_data[cx][cy] = self.legend["path"]
                break
            map_data[cx][cy] = self.legend["candidate"]
            seen.add((cx, cy))    
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                tx, ty = cx + dx, cy + dy
                if 0 <= tx < self.rows and 0 <= ty < self.cols and (tx, ty) not in seen and map_data[tx][ty] != self.legend["obstacle"]:
                    current = (tx, ty)
                    seen.add(current)
                    parent[current] = (cx, cy)
                    if self.legend["slow"] == map_data[tx][ty]:
                        heapq.heappush(heap, (self.distance(current, target) * 2, tx, ty))
                    else:
                        heapq.heappush(heap, (self.distance(current, target), tx, ty))
            
            
            steps.append([row[:] for row in map_data])

    def bfs(self, start, target, map_data, seen, parent, steps, cx, cy):
        queue = [(0, cx, cy)]
        while queue:
            dist, cx, cy = queue.pop(0)
            if (cx, cy) == target:
                map_data[cx][cy] = self.legend["path"]
                break
            map_data[cx][cy] = self.legend["candidate"]
            seen.add((cx, cy))    
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                tx, ty = cx + dx, cy + dy
                if 0 <= tx < self.rows and 0 <= ty < self.cols and (tx, ty) not in seen and map_data[tx][ty] != self.legend["obstacle"]:
                    current = (tx, ty)
                    seen.add(current)
                    parent[current] = (cx, cy)
                    if self.legend["slow"] == map_data[tx][ty]:
                        queue.append((self.distance(current, target) * 2, tx, ty))
                    else:
                        queue.append((self.distance(current, target), tx, ty))
            
            
            steps.append([row[:] for row in map_data])

    def dfs(self, start, target, map_data, seen, parent, steps, cx, cy):
        stack = [(0, cx, cy)]
        while stack:
            dist, cx, cy = stack.pop()
            if (cx, cy) == target:
                map_data[cx][cy] = self.legend["path"]
                break
            map_data[cx][cy] = self.legend["candidate"]
            seen.add((cx, cy))    
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                tx, ty = cx + dx, cy + dy
                if 0 <= tx < self.rows and 0 <= ty < self.cols and (tx, ty) not in seen and map_data[tx][ty] != self.legend["obstacle"]:
                    current = (tx, ty)
                    seen.add(current)
                    parent[current] = (cx, cy)
                    if self.legend["slow"] == map_data[tx][ty]:
                        stack.append((self.distance(current, target) * 2, tx, ty))
                    else:
                        stack.append((self.distance(current, target), tx, ty))
            
            
            steps.append([row[:] for row in map_data])   
