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

def simplifier_clause(S, clause) :
    res = []
    for c in clause :
        for s in S :
            if abs(c) == s[0] :
                val = c * s[1]
                if val > 0 :
                    res.append(c)
    return res

def test_consistance(C, S) :
    consistent = True
    i = 0
    while i < len(C) and consistent :
        nb_false = 0
        tmp = C[i].copy()
        for affectation in S :
            X = affectation[0]
            v = affectation[1]
            litteral = find_litteral(X, C[i])
            # Si la variable est dans la clause
            if litteral :
                if litteral * v < 0 :
                    tmp.remove(litteral)
        if len(tmp) == 0 :
            consistent = False
            return []
        i = i + 1
    return tmp

def variables_affectees(S) :
    variables_affectees = []
    for affectation in S :
        variables_affectees.append(affectation[0])
    return variables_affectees

def choix_variable(variables, S, clauses_pas_affectees_faux) :
    variables_aff = variables_affectees(S)
    if len(clauses_pas_affectees_faux) == 1 :
        for c in clauses_pas_affectees_faux :
            if abs(c) not in variables_aff :
                if c * 1 > 0 :
                    return (abs(c), 1, None)
                else :
                    return (abs(c), -1, None)
    for c in variables :
        if c not in variables_aff :
            return (c, 1, -1)
    return None


def dpll(variables, clauses) :
    n = len(variables)
    done = False
    S = []
    nb_echecs = 0
    while not done:
        res_test_consistance =  test_consistance(clauses, S)
        if len(res_test_consistance) > 0:
            if len(S) == n:
                done = True
            else:
                var = choix_variable(variables, S, res_test_consistance)
                S.append(var)
        else :
            nb_echecs = nb_echecs + 1
            affectation = S.pop()
            while len(S) > 0 and affectation[2] is None:
                affectation = S.pop()
            if affectation[2] is not None:
                S.append((affectation[0], affectation[1] * (-1), None))
            else:
                done = True
    print(nb_echecs)
    return S


if __name__ == '__main__':
    clauses, variables = read_cnf('uf20-01.cnf')
    #c = [[1,-2, 4], [-3,4], [-1,-3]]
    #s = [(1,1,-1), (2,+1,-1), (3,1,-1)]
    #a = test_consistance(c, s)
    #print(a)

    start_time = time.time()
    a = dpll(variables, clauses)
    print("Temps d'execution de dpll : {}".format(time.time() - start_time))
    print(a)
    exit(0)



