import base64
import heapq
import io
import random
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Agg')  
class MapPath:
    def __init__(self, rows, cols, density=0.1,slow=False):
        self.slow=slow
        self.rows = rows
        self.cols = cols
        self.map = [[0 for _ in range(cols)] for _ in range(rows)]
        self.legend = {"empty": 0, "obstacle": 1, "candidate": 2, "path": 3, "target": 4, "slow": 5}
        
        for i in range(rows):
            for j in range(cols):
                if random.random() < density:
                    if self.slow==0:
                        self.map[i][j] = self.legend["obstacle"]
                    else:
                        if self.slow:
                            self.map[i][j] = random.choice([self.legend["obstacle"],self.legend["slow"]])
        
        self.map[0][0] = 0     
        self.map[rows - 1][cols - 1] = 0     

    def distance(self, current, target):
        return ((target[0] - current[0])**2 + abs(target[1] - current[1])**2)**0.5
    def dijkstra(self, start, target, map_data, rows, cols, seen, parent, ax, steps, cx, cy):
        ax.set_title("Pathfinding Visualization - Dijkstra")
        queue = [(0, cx, cy)]
        while queue:
            dist, cx, cy = heapq.heappop(queue)
            if (cx, cy) == target:
                map_data[cx][cy] = self.legend["path"]
                break
            map_data[cx][cy] = self.legend["candidate"]
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                tx, ty = cx + dx, cy + dy
                if 0 <= tx < rows and 0 <= ty < cols and (tx, ty) not in seen and map_data[tx][ty] != self.legend["obstacle"]:
                    current = (tx, ty)
                    seen.add(current)
                    parent[current] = (cx, cy)
                    queue.append((self.distance(current, target), tx, ty))
                    map_data[tx][ty] = self.legend["candidate"]
            ax.imshow(map_data, cmap='viridis', interpolation='nearest')
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')
            steps.append(image_base64)
            buf.close()
    def astar(self, start, target,map_data,rows,cols,seen,parent,ax,steps,cx,cy):
        ax.set_title("Pathfinding Visualization")
        heap = [(0, cx, cy)]
        while heap:
            dist, cx, cy = heapq.heappop(heap)
            if (cx, cy) == target:  
                map_data[cx][cy] = self.legend["path"]
                break
            map_data[cx][cy] = self.legend["candidate"]
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                tx, ty = cx + dx, cy + dy
                if 0 <= tx < rows and 0 <= ty < cols and (tx, ty) not in seen and map_data[tx][ty] != self.legend["obstacle"]:
                    current = (tx, ty)
                    seen.add(current)
                    parent[current] = (cx, cy)
                    if self.legend["slow"] == map_data[tx][ty]:
                        heapq.heappush(heap, (self.distance(current, target) * 2, tx, ty))
                    else:
                        heapq.heappush(heap, (self.distance(current, target), tx, ty))
                    map_data[tx][ty] = self.legend["candidate"]
            ax.imshow(map_data, cmap='viridis', interpolation='nearest')
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')
            steps.append(image_base64)
            buf.close()
    def bfs(self,start,target,map_data,rows,cols,seen,parent,ax,steps,cx,cy):
        ax.set_title("Pathfinding Visualization")
        queue = [(0, cx, cy)]
        while queue:
            dist, cx, cy = queue.pop(0)
            if (cx, cy) == target:  
                map_data[cx][cy] = self.legend["path"]
                break
            map_data[cx][cy] = self.legend["candidate"]
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                tx, ty = cx + dx, cy + dy
                if 0 <= tx < rows and 0 <= ty < cols and (tx, ty) not in seen and map_data[tx][ty] != self.legend["obstacle"]:
                    current = (tx, ty)
                    seen.add(current)
                    parent[current] = (cx, cy)
                    if self.legend["slow"] == map_data[tx][ty]:
                        queue.append((self.distance(current, target) * 2, tx, ty))
                    else:
                        queue.append((self.distance(current, target), tx, ty))
            ax.imshow(map_data, cmap='viridis', interpolation='nearest')
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')
            steps.append(image_base64)
            buf.close()
    def dfs(self,start,target,map_data,rows,cols,seen,parent,ax,steps,cx,cy):
        ax.set_title("Pathfinding Visualization")
        stack = [(0, cx, cy)]
        while stack:
            dist, cx, cy = stack.pop() 
            if (cx, cy) == target:  
                map_data[cx][cy] = self.legend["path"]
                break
            map_data[cx][cy] = self.legend["candidate"]
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                tx, ty = cx + dx, cy + dy
                if 0 <= tx < rows and 0 <= ty < cols and (tx, ty) not in seen and map_data[tx][ty] != self.legend["obstacle"]:
                    current = (tx, ty)
                    seen.add(current)
                    parent[current] = (cx, cy)
                    if self.legend["slow"] == map_data[tx][ty]:
                        stack.append((self.distance(current, target) * 2, tx, ty))
                    else:
                        stack.append((self.distance(current, target), tx, ty))
            ax.imshow(map_data, cmap='viridis', interpolation='nearest')
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')
            steps.append(image_base64)
            buf.close()
    def route(self, start, target, method):
        rows = self.rows
        cols = self.cols
        map_data = [row[:] for row in self.map]
        seen = set([start])
        parent = {}
        cx, cy = start
        map_data[target[0]][target[1]] = self.legend["target"]
        map_data[cx][cy] = self.legend["candidate"]
        steps = []
        fig, ax = plt.subplots(figsize=(5, 5))
        if method == "A*":
            self.astar(start, target, map_data, rows, cols, seen, parent, ax, steps, cx, cy)
        elif method == "BFS":
            self.bfs(start, target, map_data, rows, cols, seen, parent, ax, steps, cx, cy)
        elif method == "DFS":
            self.dfs(start, target, map_data, rows, cols, seen, parent, ax, steps, cx, cy)
        elif method == "Dijkstra":
            self.dijkstra(start, target, map_data, rows, cols, seen, parent, ax, steps, cx, cy)
        
        path = []
        current = target
        while current in parent:
            path.append(current)
            current = parent[current]
        path.append(start)
        for px, py in path:
            map_data[px][py] = self.legend["path"]
        ax.imshow(map_data, cmap='viridis', interpolation='nearest')
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        steps.append(image_base64)
        buf.close()
        plt.close('all')
        return steps
