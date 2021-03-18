

import numpy as np
import time

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
        raise Exception("File Reading failed : the number of clauses doesn't match")
    variables = list(np.arange(1,nb_variables+1))
    return clauses, variables

def find_litteral(X, clause) :
    for i in range(len(clause)) :
        if abs(clause[i]) == X :
            return clause[i]
    return None

def find_affectation(l, S) :
    for s in S :
        if s[0] == abs(l) :
            return l * s[1] > 0
    return None


def test_consistance(C, S) :
    clauses_unitaires = set()
    for clause in C :
        clauses_bool = [find_affectation(l,S) for l in clause]
        if not any(clauses_bool) :
            nb_not_contradicted = clauses_bool.count(None)
            if nb_not_contradicted == 0 :
                return False, clauses_unitaires
            elif nb_not_contradicted == 1 :
                index = clauses_bool.index(None)
                clauses_unitaires.add(clause[index])
    return True, clauses_unitaires



def choisir_triplet(S, variables_a_affecter, clauses_unitaires) :
    i = 0
    if clauses_unitaires :
        var = clauses_unitaires.pop()
        variables_a_affecter.remove(abs(var))
        if var > 0 :
            return var, 1, None
        else :
            return abs(var), -1, None
    else :
        var = variables_a_affecter.pop()
        return var, 1, -1


def dpll(variables, clauses) :
    n = len(variables)
    done = False
    S = []
    variables_restantes = set(variables)
    while not done :
        resultat_test = test_consistance(clauses,S)
        is_consistent = resultat_test[0]
        clauses_unitaires = resultat_test[1]
        if is_consistent :
            if len(S) == n :
                done = True
            else :
                triplet = choisir_triplet(S, variables_restantes, clauses_unitaires)
                S.append(triplet)
        else :
            triplet = S.pop()
            variables_restantes.add(triplet[0])
            while len(S) > 0 and triplet[2] is None :
                triplet = S.pop()
                variables_restantes.add(triplet[0])
            if triplet[2] is not None :
                new_triplet = (triplet[0], triplet[2], None)
                S.append(new_triplet)
                variables_restantes.remove(new_triplet[0])
            else :
                done = True
    S.sort(key=lambda tup: tup[0])
    return S

if __name__ == '__main__':
    clauses, variables = read_cnf('uf20-01.cnf')
    c = [[1, -2, 4], [-3, 4], [-1, -3]]
    a = dpll([1,2,3,4], c)
    print(a)
    start_time = time.time()
    S = dpll(variables, clauses)
    print("Temps d'execution de dpll : {}".format(time.time() - start_time))
    print(S)
    print(test_consistance(clauses,S))
    exit(0)


