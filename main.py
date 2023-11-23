from constraint import *
import sys
from vehiculos import Vehiculos


def main(file):
    with open(file, "r") as f:
        lectura = f.readlines()

    filas = int(lectura[0][0])
    columnas = int(lectura[0][2])

    dominio_entero = calc_dominio_entero(columnas, filas)
    dominio_electrico = calc_dominio_electrico(lectura[1])
    dominio_no_electrico = calc_dominio_no_electrico(dominio_electrico, dominio_entero)
    variables = crear_variables(lectura)

    problem = Problem()
    for v in variables:
        if v.freezer == "C":
            problem.addVariable(v.calc_v(), dominio_electrico)
        else:
            problem.addVariable(v.calc_v(), dominio_no_electrico)

    problem.addConstraint(AllDifferentConstraint())
    for i in variables:
        for j in variables:
            if i != j:
                if i.type == "TSU" and j.type == "TNU":
                    problem.addConstraint(prioridad, (i.calc_v(), j.calc_v()))
    print(len(problem.getSolutions()))


def prioridad(vehiculo_i, vehiculo_j):
    if vehiculo_i[0] == vehiculo_j[0]:
        return vehiculo_i[1] > vehiculo_j[0]
    return True


def crear_variables(lectura):
    lista = []
    for i in range(2, len(lectura)):
        v = Vehiculos(lectura[i][0], lectura[i][2:5], lectura[i][6])
        lista.append(v)
    return lista


def calc_dominio_no_electrico(dominio_electrico, dominio_entero):
    dominio_no_electrico = []
    for tupla in dominio_entero:
        if tupla not in dominio_electrico:
            dominio_no_electrico.append(tupla)
    return dominio_no_electrico


def calc_dominio_electrico(lista_elec):
    dominio_electrico = []
    lect_temp = ""
    indice = 3

    while indice < len(lista_elec) - 1:
        lec = lista_elec[indice:indice + 5]
        indice += 5
        tupla = (int(lec[1]), int(lec[3]))
        dominio_electrico.append(tupla)
    return dominio_electrico


def calc_dominio_entero(columnas, filas):
    dominio_entero = []
    for col in range(columnas):
        for row in range(filas):
            pos = (row+ 1, col + 1)
            dominio_entero.append(pos)
    return dominio_entero


if __name__ == "__main__":
    main(sys.argv[1])
