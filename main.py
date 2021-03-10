# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import numpy as np
import copy
import time
import threading
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

def find_value(X, v, clause) :
    for litteral in clause :
        if abs(litteral) == X :
            return v * litteral
    return None
def test_consistance(C, S) :
    consistent = True
    #start_time = time.time()
    nb_clauses_unitaires = 0
    i = 0
    while i < len(C) and consistent :
        nb_false = 0
        for affectation in S :
            X = affectation[0]
            v = affectation[1]
            value = find_value(X,v,C[i])
            if value and value < 0 :
                nb_false = nb_false + 1
        if nb_false == len(C[i]):
            consistent = False
        elif nb_false == len(C[i]) - 1 :
            nb_clauses_unitaires = nb_clauses_unitaires + 1
        i = i + 1
    #print(time.time() - start_time)
    return consistent, nb_clauses_unitaires

def next_var_to_set(S, liste_variables) :
    affected_variables = []
    for s in S:
        affected_variables.append(s[0])
    var = [x for x in liste_variables if x not in affected_variables][0]
    return var

def find_S(variables, clauses) :
    n = len(variables)
    done = False
    S = []
    nb_echecs = 0
    while not done:
        if test_consistance(clauses, S)[0]:
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
    #s = [(1,1,-1), (2,+1,-1), (3,-1,None),(4,1,-1)]
    s = [(1,1,-1),(2,+1,-1),(3,1, -1)]
    a = test_consistance(c, s)
    print(a)

    start_time = time.time()
    a = find_S(variables, clauses)
    print(time.time() - start_time)
    print(a)
    exit(0)



