from Basic_Attributes import *  
from Environment import comparewell, mazeSetup

def distance_metric(a, b):
    x = abs(a[0] - b[0])
    y = abs(a[1] - b[1])
    return x + y

def greedy_bfs(g, e, d):
    started = time.time()
    pq , at , es  , visited = [] , {} , [] , set()
    counter = 0

    pq.append((0, e))
    visited.add(e)

    while pq:
        pq.sort(key=lambda x: x[0])  
        c, n = pq.pop(0) 
        temp = [] 
        counter += 1

        if n == d:
            p = []
            while n in at:
                p.append(n)
                n = at[n]
            p.append(e)
            return p[::-1], es, counter, time.time() - started

        x = n[0]
        y = n[1]

        for di in DIRECTIONS:
            nei = (x + di[0], y + di[1])
            if (0 <= nei[0] < len(g[0])) and (0 <= nei[1] < len(g)):
                if (g[nei[1]][nei[0]] == 0) and (nei not in visited):
                    visited.add(nei)
                    at[nei] = n
                    pq.append((distance_metric(nei, d), nei))
        
        for node in pq :
            temp.append(node[-1])
        es.append(temp)

    return None, es, counter, time.time() - started

def a_star(g, e, d):
    t = time.time()
    pq , am , tc , pc , vl , tj = [] , {} , {e:0}  , {e: distance_metric(e, d)} , set () , []
    
    counter = 0

    pq.append((0, e))

    while pq:
        pq.sort(key=lambda x: x[0]) 
        cost, n = pq.pop(0)  
        counter += 1

        if n == d:
            p = []
            while n in am:
                p.append(n)
                n = am[n]
            p.append(e)
            return p[::-1], tj, counter, time.time() - t

        vl.add(n)

        x = n[0]
        y = n[1]

        for di in DIRECTIONS:
            nei = (x + di[0], y + di[1])

            if (0 <= nei[0] < MAZE_WIDTH) and (0 <= nei[1] < MAZE_HEIGHT):
                if g[nei[1]][nei[0]] == 0:
                    ic = tc[n] + 1
                    if (nei not in vl) or (ic < tc.get(nei, float('inf'))):
                        am[nei] , tc[nei] = n , ic
                        pc[nei] = ic + distance_metric(nei, d)
                        pq.append((pc[nei], nei))
        temp = []
        for i in pq :
            temp.append(i[1])

        tj.append(temp)

    return None, tj, counter, time.time() - t
