# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import numpy as np
import time

def read_cnf(filename) :
    with open(filename, "r") as file :
        data = file.read().split()
        index = data.index('length')
        clause_length = int(data[index+2])
        index = data.index('cnf')
        data = data[index+1:]
        nb_variables = int(data[0])
        nb_clauses = int(data[1])
        data = data[2:]
        data = list(filter(('0').__ne__,data))[:-1]
    clauses = np.array(list(map(int,data)))
    clauses = np.ndarray.tolist(clauses.reshape(nb_clauses, clause_length))
    variables = np.ndarray.tolist(np.arange(1,nb_variables+1))
    return clauses, variables

def find_litteral(X, clause) :
    for litteral in clause :
        if abs(litteral) == X :
            return litteral
    return None

def test_consistance(C, S) :
    consistent = True
    clauses_unitaires = []
    i = 0
    while i < len(C) and consistent :
        nb_false = 0
        nb_litteraux = len(C[i])
        c = None
        for affectation in S :
            X = affectation[0]
            v = affectation[1]
            litteral = find_litteral(X, C[i])
            if litteral :
                if litteral * v < 0 :
                    nb_false = nb_false + 1
                else :
                    c = litteral
        if nb_false == nb_litteraux:
            consistent = False
        elif nb_false == nb_litteraux - 1 :
            if c  :
                clauses_unitaires.append(c)
        i = i + 1
    return consistent, clauses_unitaires

def next_var_to_set(S, liste_variables) :
    affected_variables = []
    for s in S:
        affected_variables.append(s[0])

    var = [x for x in liste_variables if x not in affected_variables][0]
    return var

def choix_affectation(X, valeurs) :
    if len(valeurs) == 0 :
        return (X, 1, -1)
    if len(valeurs) == 1 :
        return (X, valeurs[0], - valeurs[0])


def dpll(variables, clauses) :
    n = len(variables)
    done = False
    S = []
    nb_echecs = 0
    while not done:
        res_test_consistance =  test_consistance(clauses, S)
        if res_test_consistance[0]:
            if len(S) == n:
                done = True
            else:
                S.append((next_var_to_set(S, variables), 1, -1))
        else:
            nb_echecs = nb_echecs + 1
            affectation = S.pop()
            while len(S) > 0 and affectation[2] is None:
                affectation = S.pop()
            if affectation[2] is not None:
                S.append((affectation[0], -1, None))
            else:
                done = True
    print(nb_echecs)
    return S


if __name__ == '__main__':
    clauses, variables = read_cnf('uf20-01.cnf')
    c = [[1,-2, 4], [-3,4], [-1,-3]]
    s = [(1,1,-1), (2,+1,-1), (3,-1,None),(4,1,-1)]
    a = test_consistance(c, s)
    print(a)

    start_time = time.time()
    a = dpll(variables, clauses)
    print(a)
    print(time.time() - start_time)
    print(a)
    exit(0)



