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

def read_cnf(filename) :
    clauses = []
    with open(filename, "r") as file :
        for line in file :
            if '%' in line :
                break
            if line.startswith("p") :
                data = line.split()
                nb_variables = int(data[2])
                nb_clauses = int(data[3])
            elif line[0] != 'c' :
                data = line.split()
                data = data[:-1]
                map_object = map(int,data)
                data = list(map_object)
                clauses.append(data)
    if len(clauses) != nb_clauses :
        print(len(clauses))
        print(nb_clauses)
        print(clauses)
        raise Exception("File Reading failed : the number of clauses doesn't match")
    variables = list(np.arange(1,nb_variables+1))
    return clauses, variables




def find_litteral(X, clause) :
    for litteral in clause :
        if abs(litteral) == X :
            return litteral
    return None

def test_consistance(C, S) :
    consistent = True
    i = 0
    clauses_unitaires = []
    while i < len(C) and consistent :
        tmp = C[i].copy()
        for affectation in S :
            X = affectation[0]
            v = affectation[1]
            litteral = find_litteral(X, tmp)
            # Si la variable est dans la clause
            if litteral :
                if litteral * v < 0 :
                    tmp.remove(litteral)
        if len(tmp) == 0 :
            consistent = False
        if len(tmp) == 1 and tmp[0] not in clauses_unitaires  :
            clauses_unitaires.append(tmp)
        i = i + 1
    return consistent, clauses_unitaires



def choix_variable(variables, clauses_unitaires) :
    for c in clauses_unitaires :
        c = c[0]
        if abs(c) in variables :
            if c * 1 > 0 :
                return (abs(c), 1, None)
            else :
                return (abs(c), -1, None)
    return(variables[0], 1, -1)


def dpll(variables, clauses) :
    n = len(variables)
    done = False
    S = []
    variables_a_affecter = variables.copy()
    nb_echecs = 0
    while not done:
        res_test_consistance =  test_consistance(clauses, S)
        if res_test_consistance[0]:
            if len(S) == n:
                done = True
            else:
                var = choix_variable(variables_a_affecter, res_test_consistance[1])
                S.append(var)
                variables_a_affecter.remove(var[0])
        else :
            nb_echecs = nb_echecs + 1
            affectation = S.pop()
            variables_a_affecter.append(affectation[0])
            while len(S) > 0 and affectation[2] is None:
                affectation = S.pop()
                variables_a_affecter.append(affectation[0])
            if affectation[2] is not None:
                S.append((affectation[0], affectation[1] * (-1), None))
                variables_a_affecter.remove(affectation[0])
            else:
                done = True
    print(nb_echecs)
    S.sort(key=lambda tup: tup[0])
    return S


if __name__ == '__main__':
    # TO DO : ADD LITTERAUX PURS
    # TO DO : ADD MODELES PARTIELS
    # TO DO : TESTER SI CA MARCHE AVEC 100
    clauses, variables = read_cnf('uf20-01.cnf')
    c = [[1,-2, 4], [-3,4], [-1,-3]]
    #s = [(1,1,-1),(2,1,-1),(3,1), (4,1,-1)]
    #s = [(1,1,-1), (2,+1,-1), (3,1,None),[4,-1,-1]]
    #a = test_consistance(c, s)
    #print(a)
    #c = [[1,2,-1,3],[-3,2,-1,3]]
    start_time = time.time()
    a = dpll(variables, clauses)
    print("Temps d'execution de dpll : {}".format(time.time() - start_time))
    print(a)
    exit(0)



