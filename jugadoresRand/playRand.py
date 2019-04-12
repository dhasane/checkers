import random as rand

def player(E,M,J):
    if len(M)==0:
        return None
    return rand.choice(M)
