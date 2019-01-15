#!/usr/bin/env python3

__author__ = "Andrea Fioraldi"
__mail__ = "fioraldi.1692419@studenti.uniroma1.it"

import random
import networkx as nx

def random_graph(n, p, seed=None):
    """p = probability for edge creation"""
    
    G = nx.generators.classic.empty_graph(n)

    if not seed is None:
        random.seed(seed)

    for u in range(n):
        for v in range(u+1,n):
            if random.random() < p:
                G.add_edge(u,v)
    
    for (u, v) in G.edges():
        G.edges[u,v]['weight'] = random.randint(0,10)
    
    return G

def draw_mst(G, mst):
    import matplotlib.pyplot as plt
    
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels = True)  # with_labels=true is to show the node number in the output graph
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels, font_size = 11) #    prints weight on all the edges

    for u,v,w in mst: 
        nx.draw_networkx_edges(G, pos, edgelist = [(u, v)], width = 2.5, alpha = 0.6, edge_color = 'r')

    plt.show()


def is_in_mst(G, e):
    visited = [False]*(len(G.nodes())) 
    e_w = G.edges[e]["weight"]
    
    def aux(v):
        visited[v] = True
        r = True
        
        for i in G.neighbors(v):
            if G.edges()[v,i]["weight"] >= e_w:
                continue
            if i == e[1]:
                return False
            if visited[i] == False: 
                r = r and aux(i)
        
        return r
    
    return aux(e[0])


def kruskal(G, e=None): 
    ''' e!=None forces to include edge e in the mst'''
    
    def find(parent, i):
        if parent[i] == i:
            return i
        return find(parent, parent[i])

    def union(parent, order, x, y):
        rx = find(parent, x)
        ry = find(parent, y)
        if order[rx] < order[ry]:
            parent[rx] = ry
        elif order[rx] > order[ry]:
            parent[ry] = rx
        else :
            parent[ry] = rx
            order[rx] += 1

    mst = []
    
    i = 0
    j = 0
    
    s_edges = sorted(G.edges(), key=lambda x: G.edges[x]['weight'])
    if e is not None:
        s_edges.remove(e)
        s_edges = [e] + s_edges
        
    parent = []
    rank = [] 

    for n in G.nodes(): 
        parent.append(n)
        rank.append(0)
  
    while j < len(G.nodes())-1: 
        if i == len(s_edges): break
        
        u,v = s_edges[i]
        w = G.edges[u,v]['weight']
        
        i += 1
        x = find(parent, u)
        y = find(parent, v)

        if x != y: 
            j += 1 
            mst.append((u,v,w))
            union(parent, rank, x, y)
    
    return mst


def mst_from_edge(G, e):
    if not is_in_mst(G, e):
        raise Exception("edge %s cannot be in a MST" % str(e))
    return kruskal(G, e)


def test():
    fails = 0
    for i in range(100):
        print("\033[A\33[2KT\rtest progress: %d of 100" % i)
        
        G = random_graph(random.randint(10,200), random.random() % 0.9 + 0.1)
        if len(G.edges()) < 2: continue #skip dump graphs
        
        e = random.sample(G.edges(), 1)[0]
        
        mst_1 = kruskal(G)
        mst_2 = kruskal(G, e)
        f = True
        for x in mst_2: 
            if (x[0],x[1]) == e: f = False
        if f:
            print ("e not in mst")
        
        sw_1 = sum(map(lambda x: x[2], mst_1))
        sw_2 = sum(map(lambda x: x[2], mst_2))
        
        iim = is_in_mst(G,e)
        if iim and sw_1 != sw_2:
            fails += 1
        if not iim and sw_1 >= sw_2:
            fails += 1
    if fails != 0:
        print ("your implementation is bugged!")
    else:
        print ("no error")


if __name__ == "__main__":
    test()
    
    G = random_graph(15, 0.2)
    e = random.sample(G.edges(), 1)[0]
    
    if is_in_mst(G, e):
        print (e,"is in mst!")
        mst = kruskal(G, e)
        draw_mst(G, mst)
    else:
        print (e,"is not in mst!")
        mst = kruskal(G, None)
        draw_mst(G, mst)
    

