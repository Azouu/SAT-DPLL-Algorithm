

import numpy as np
import time
import operator
from collections import Counter

modele_partiel = False
all_solutions = True

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

def find_affectation(l, S) :
    for s in S :
        if s[0] == abs(l) :
            return l * s[1] > 0
    return None

def test_consistance(C, S) :
    clauses_unitaires = set()
    clauses_simplifiees = []
    cpt_true = 0
    for clause in C :
        clause_bool = [find_affectation(l,S) for l in clause]
        if not any(clause_bool) :
            nb_not_contradicted = clause_bool.count(None)
            if nb_not_contradicted == 0 :
                return False, clauses_unitaires, clauses_simplifiees
            elif nb_not_contradicted == 1 :
                index = clause_bool.index(None)
                clauses_unitaires.add(clause[index])
            else :
                clauses_simplifiees.append([l for l, bool in zip(clause, clause_bool) if bool is None])
        elif modele_partiel :
            cpt_true = cpt_true + 1

    #verif = [x for x in clauses_unitaires if -x in clauses_unitaires]
    #if verif :
    #    return False, clauses_unitaires, clauses_simplifiees
    return True, clauses_unitaires, clauses_simplifiees, cpt_true



def choisir_triplet(S, variables_a_affecter, clauses_unitaires, clauses_simplifiees) :
    if clauses_unitaires :
        while clauses_unitaires :
            var = clauses_unitaires.pop()
            if -var not in clauses_unitaires :
                variables_a_affecter.remove(abs(var))
                if var > 0 :
                   S.append((var, 1, None))
                else :
                    S.append((abs(var), -1, None))
    else :
        flat = set([item for sublist in clauses_simplifiees for item in sublist])
        purs = [x for x in flat if -x not in flat]
        if purs :
            while purs :
                var = purs.pop()
                variables_a_affecter.remove(abs(var))
                if var > 0:
                    S.append((var, 1, -1))
                else:
                    S.append((abs(var), -1, 1))
        else:
            dict = {key:0 for key in variables_a_affecter}
            for sublist in clauses_simplifiees :
                for l in sublist :
                    dict[abs(l)] = dict[abs(l)] + 1/len(sublist)
            var = max(dict, key=dict.get)
            variables_a_affecter.remove(var)
            S.append((var, 1, -1))

# TODO Vérifier Modèles partiels
def dpll(variables, clauses) :
    n = len(variables)
    done = False
    S = []
    variables_restantes = set(variables)
    nb_erreurs = 0
    while not done :
        resultat_test = test_consistance(clauses,S)
        is_consistent = resultat_test[0]
        clauses_unitaires = resultat_test[1]
        if is_consistent :
            if modele_partiel and resultat_test[3] == len(clauses):
                    done = True
            elif len(S) == n :
                    done = True
            else :
                choisir_triplet(S, variables_restantes, clauses_unitaires, resultat_test[2])
        else :
            nb_erreurs = nb_erreurs + 1
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
    print("Nombre d'erreurs = {}".format(nb_erreurs))
    S.sort(key=lambda tup: tup[0])
    print(S)
    return S


def dpll_all_solutions(variables, clauses) :
    n = len(variables)
    nb_erreurs = 0
    done = False
    S = []
    variables_restantes = set(variables)
    while not done :
        resultat_test = test_consistance(clauses,S)
        is_consistent = resultat_test[0]
        clauses_unitaires = resultat_test[1]
        if is_consistent :
            if len(S) == n :
                resultat = S.copy()
                #print(resultat)
                resultat.sort(key=lambda tup: tup[0])
                print(resultat)
                triplet = S.pop()
                variables_restantes.add(triplet[0])
                while len(S) > 0 and triplet[2] is None:
                    triplet = S.pop()
                    variables_restantes.add(triplet[0])
                if triplet[2] is not None:
                    new_triplet = (triplet[0], triplet[2], None)
                    S.append(new_triplet)
                    variables_restantes.remove(new_triplet[0])
                else:
                    done=True
            else :
                choisir_triplet(S, variables_restantes, clauses_unitaires, resultat_test[2])
        else :
            nb_erreurs = nb_erreurs + 1
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
    print("Nombre d'erreurs : {}".format(nb_erreurs))
    return S


if __name__ == '__main__':
    clauses, variables = read_cnf('jnh1.cnf.txt')
    c = [[1, -2, 4], [-3, 4], [-1, -3]]
    #print(test_consistance(c,[(1, -1, None), (2, 1, -1), (3, 1, -1), (4, 1, None)]))
    #a = dpll([1,2,3,4], c)
    #print(a)
    start_time = time.time()
    S = dpll(variables, clauses)
    print("Temps d'execution de dpll : {}".format(time.time() - start_time))
    exit(0)


