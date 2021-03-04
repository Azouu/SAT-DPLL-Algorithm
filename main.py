# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import numpy as np

def read_cnf(filename) :
    with open("cnf.txt", "r") as file :
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
    clauses = clauses.reshape(nb_clauses, clause_length)
    variables = np.arange(1,nb_variables+1)
    return clauses, variables

def test_consistance(clauses, s) :
    # itérer sur clauses
    # chaque variables différente de -1
    # si count vaut 0 -> inconsistance, sinon on renvoie 1
    for c in clauses :
        for aff in s :


if __name__ == '__main__':
    clauses, variables = read_cnf('cnf.txt')
    print(clauses)
    print(variables)
    exit(0)



