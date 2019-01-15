from z3 import *
import re, random


def test(D, w):
    G = sorted(w.keys())
    n = len(D)
    
    ## primal

    o = Optimize()

    x = {}
    for c in xrange(len(G)):
        Gk = G[c]
        x[Gk] = Real("x%d" % c)
        o.add(x[Gk] >= 0)
    z = {}
    for i in xrange(0,n+1):
        for j in xrange(0,n+1):
            if i < j and D[i:j] in G:
                z[i] = z.get(i, {})
                z[i][j] = Real("z%d%d" % (i,j))
                o.add(z[i][j] >= 0)

    for i in xrange(0,n+1):
        for j in xrange(0,n+1):
            if i < j and D[i:j] in G:
                o.add(x[D[i:j]] - z[i][j] >= 0)

    usc = []
    for j in xrange(0,n+1):
        if D[0:j] in G:
            usc.append(z[0][j])
    o.add(Sum(usc) == 1)

    for v in xrange(1,n):
        usc = []
        for j in xrange(0,n+1):
            if D[v:j] in G:
                usc.append(z[v][j])
        ent = []
        for i in xrange(0,n+1):
            if D[i:v] in G:
                ent.append(z[i][v])
        o.add(Sum(usc) == Sum(ent))


    h = o.minimize(Sum([w[Gk]*x[Gk] for Gk in G]))

    #print o.check()
    #print o.lower(h), o.model()
    
    if o.check() != sat:
        return
    value = o.lower(h)
    
    ## dual

    p = {}
    q = {}
    for i in xrange(0,n+1):
        if i == n: p[i] = 0
        else: p[i] = Real("p%d"%i)
        
        for j in xrange(0,n+1):
            if i < j and D[i:j] in G:
                q[i] = q.get(i, {})
                q[i][j] = Real("q%d%d" % (i,j))

    o = Optimize()

    for Gk in G:
        substrs = [(a.start(), a.end()) for a in list(re.finditer(Gk , D))]
        o.add(Sum([q[i][j] for i,j in substrs]) <= w[Gk])

    for i in xrange(0,n+1):
        p[i] = Real("p%d"%i)
        for j in xrange(0,n+1):
            if i < j and D[i:j] in G:
                o.add(-q[i][j]+p[i]-p[j] <= 0)
                o.add(q[i][j] >= 0)

    h = o.maximize(p[0])

    #print o.check()
    #print o.upper(h), o.model()
    
    if o.check() != sat:
        return
    
    if not( o.upper(h) == value ):
        print "DOH!", value, o.upper(h)



def indexes(seq, start=0):
    return (i for i,_ in enumerate(seq, start=start))

alpha = "ACTG"
for c in xrange(100):
    n = random.randint(0, 30)
    D = ''.join(random.choice(alpha) for _ in range(n))
    m = random.randint(0, n)
    all_sub = list(D[i:j] for i in indexes(D) for j in indexes(D[i:], i+1))
    w = random.sample(all_sub, len(all_sub))
    w = {g: random.randint(0, 20) for g in w}
    print "test ", c
    try:
        test(D,w)
    except AttributeError:
        print("something goes wrong in Z3py")
