#!/usr/bin/env python3
"""Anexo Paper 1 — Rama D: D4 diagonal + swap de piernas.
Reproduce orden 16, firma 2/12/2, 10 órbitas de W, 2 polos, 34 órbitas.
Sin complemento como generador. Sin física. Sin kappa ni F.
"""
from collections import Counter, deque
import itertools

def compose(p, q):
    return [p[q[i]] for i in range(len(p))]

def cycles_of(p):
    seen = [False] * len(p)
    parts = []
    for i in range(len(p)):
        if not seen[i]:
            cyc = []
            j = i
            while not seen[j]:
                seen[j] = True
                cyc.append(j)
                j = p[j]
            parts.append(cyc)
    return parts

def cycle_notation(p):
    parts = [c for c in cycles_of(p) if len(c) > 1]
    return "id" if not parts else "".join(
        "(" + " ".join(str(x) for x in c) + ")" for c in parts
    )

def order_of(p):
    n = len(p)
    idn = list(range(n))
    h = list(p)
    o = 1
    while h != idn:
        h = compose(p, h)
        o += 1
        if o > 64:
            return None
    return o

def apply_pos(v, g):
    w = [0] * 8
    for i, val in enumerate(v):
        w[g[i]] = val
    return tuple(w)

# Rama D generators
S = [4, 5, 6, 7, 0, 1, 2, 3]          # swap legs
R = [1, 2, 3, 0, 5, 6, 7, 4]          # rotate both columns
G = [0, 3, 2, 1, 4, 7, 6, 5]          # reflect both columns

def generate(gens):
    id8 = list(range(8))
    seen = {tuple(id8)}
    out = [id8]
    q = deque([id8])
    while q:
        g = q.popleft()
        for s in gens:
            h = compose(s, g)
            th = tuple(h)
            if th not in seen:
                seen.add(th)
                out.append(h)
                q.append(h)
    return out

def main():
    group = generate([S, R, G])
    print("orden", len(group))
    print("S", cycle_notation(S), "ord", order_of(S))
    print("R", cycle_notation(R), "ord", order_of(R))
    print("G", cycle_notation(G), "ord", order_of(G))
    print("ordenes", dict(Counter(order_of(g) for g in group)))
    print("abeliano", all(compose(a, b) == compose(b, a) for a in group for b in group))
    print("hay_orden_4", any(order_of(g) == 4 for g in group))
    print("orbitas_V", sum(2 ** len(cycles_of(g)) for g in group) / len(group))

    W = list(itertools.combinations(range(8), 4))
    seen = set()
    norb = 0
    total = 0
    for s in W:
        fs = frozenset(s)
        if fs in seen:
            continue
        orb = set([fs])
        st = [fs]
        while st:
            x = st.pop()
            for g in group:
                y = frozenset(g[i] for i in x)
                if y not in orb:
                    orb.add(y)
                    st.append(y)
        seen |= orb
        norb += 1
        total += len(orb)
    print("orbitas_W", norb, "suma", total)

    # firma
    def compose4(p, q):
        return [p[q[i]] for i in range(4)]

    D4 = [list(range(4))]
    S4 = {tuple(range(4))}
    q = deque([list(range(4))])
    while q:
        g = q.popleft()
        for s in ([1, 2, 3, 0], [0, 3, 2, 1]):
            h = compose4(s, g)
            if tuple(h) not in S4:
                S4.add(tuple(h))
                D4.append(h)
                q.append(h)

    def order4(p):
        id4 = list(range(4))
        h = list(p)
        o = 1
        while h != id4:
            h = compose4(p, h)
            o += 1
        return o

    sig = Counter()
    for bits in itertools.product((0, 1), repeat=4):
        stab = []
        for g in D4:
            new = [None] * 4
            for i, val in enumerate(bits):
                new[g[i]] = val
            if tuple(new) == bits:
                stab.append(g)
        n = len(stab)
        if n == 8:
            t = "D4"
        elif n == 4:
            t = "C4" if any(order4(g) == 4 for g in stab) else "V4"
        elif n == 2:
            t = "C2"
        else:
            t = str(n)
        sig[t] += 1
    print("firma", dict(sig))

    # Rama I (debe fallar)
    rotL = [1, 2, 3, 0, 4, 5, 6, 7]
    rotR = [0, 1, 2, 3, 5, 6, 7, 4]
    reflL = [0, 3, 2, 1, 4, 5, 6, 7]
    reflR = [0, 1, 2, 3, 4, 7, 6, 5]
    gi = generate([rotL, rotR, reflL, reflR, S])
    print("rama_I_orden", len(gi), "STOP" if len(gi) != 16 else "PASS")

if __name__ == "__main__":
    main()
