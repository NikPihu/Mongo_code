import random

def generate_maze():
    maze=[]

    for r in range(5):
        row=[]
        for c in range(5):
            if random.random()<0.30:
                row.append("#")
            else:
                row.append(".")
        maze.append(row)

    maze[0][0]='S'
    maze[4][0]='E'

    return maze


maze=generate_maze()
for row in maze:
    print("".join(row))


mode="graph"

graph={
    "A":["B","C"],
    "B":["A","D"],
    "C":["E","A"],
    "D":["B","F"],
    "E":["C","F"],
    "F":["D","E"]
}

print(graph)


def get_neighbors(node):
    if mode=="graph":
        return graph[node]

    row,col=node

    results=[]

    dx=[-1,1,0,0]
    dy=[0,0,1,-1]

    for i in range(4):
        newr=row+dx[i]
        newc=col+dy[i]

        if 0<=newr<len(maze) and 0<=newc<len(maze[0]):
            if maze[newr][newc]!='#':
                results.append((newr,newc))

    return results


def bfs(start,end):
    queue=[[start]]
    visited=[start]

    explored=0

    while len(queue)>0:
        path=queue.pop(0)
        node=path[-1]

        explored=explored+1

        if node==end:
            return path,explored

        for n in get_neighbors(node):
            if n not in  visited:
                visited.append(n)
                queue.append(path+[n])

    return None,explored


def dfs(start,end):
    stack=[[start]]
    visited=[start]

    explored=0

    while len(stack)>0:
        path=stack.pop()
        node=path[-1]

        explored=explored+1

        if node==end:
            return path,explored

        for n in get_neighbors(node):
            if n not in  visited:
                visited.append(n)
                stack.append(path+[n])

    return None,explored


import time
def comparison(start,end):
    t1=time.perf_counter()
    bfs_path,bfs_nodes=bfs(start,end)
    t2=time.perf_counter()-t1

    t3=time.perf_counter()
    dfs_path,dfs_nodes=dfs(start,end)
    t4=time.perf_counter()-t3

    print("----------BFS------------")
    print("Path: ",bfs_path)
    print("Nodes: ",bfs_nodes)
    print("Time: ",t2)

    print("-------DFS--------")
    print("Path: ",dfs_path)
    print("Nodes: ",dfs_nodes)
    print("Time: ",t4)

    return bfs_path,dfs_path


def show_path(path):
    if path is None:
        print("No path found")
        return

    grid=[list(row) for row in maze]

    for r,c in path:
        if grid[r][c]=='.':
            grid[r][c]='*'

    for row in grid:
        print("".join(row))


# graph search
print("\n===== GRAPH: A -> F =====")
comparison("A","F")

# maze search
mode="maze"
maze_start=(0,0)
maze_end=(4,0)
print("\n===== MAZE: S -> E =====")
bfs_path,dfs_path=comparison(maze_start,maze_end)


print("\nDFS path:")
show_path(dfs_path)


print("\nBFS path:")
show_path(bfs_path)
