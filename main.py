import random

from constraint import *
import sys
from vehiculos import Vehiculos

global ad
global filas
global columnas
ad = False


def main(file):
    with open(file, "r") as f:
        lectura = f.readlines()

    set_filas(int(lectura[0][0]))
    set_columnas(int(lectura[0][2]))

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
            if i.id != j.id:
                if i.type == "TSU" and j.type == "TNU":
                    problem.addConstraint(prioridad, (i.calc_v(), j.calc_v()))
    problem.addConstraint(adyacencia, problem._variables)
                    
    sol = problem.getSolutions()
    sols = []
    for i in range(min(10, len(sol))):
        num = random.randint(0, len(sol) - 1)
        sols.append(sol[num])

    ind = file.index(".")
    escr_salida(len(sol), sols, file[0:ind])


def escr_salida(num_sol, sols, name):
    keys = sols[0].keys()
    with open(name + ".csv", "w") as salida:
        salida.write("\"N. Sol:\"," + str(num_sol) + "\n")
        for sol in sols:
            matriz = []
            for f in range(filas):
                row = []
                for c in range(columnas):
                    row.append("-")
                matriz.append(row)
            for k in keys:
                matriz[sol[k][0] - 1][sol[k][1] - 1] = k
            for row in range(len(matriz)):
                for col in range(len(matriz[row])):
                    salida.write("\"" + matriz[row][col] + "\"")
                    if col < len(matriz[row]) - 1:
                        salida.write(",")
                    else:
                        salida.write("\n")
            salida.write("\n")


def set_ad(value):
    global ad
    ad = value


def set_filas(value):
    global filas
    filas = value


def set_columnas(value):
    global columnas
    columnas = value


def adyacencia(*args):
    for i in range(len(args)):
        vehiculo = args[i];
        for j in range(len(args)):
            vadj = args[j]
            if (i != j):
                if vehiculo[1] == vadj[1]:
                    # Esta arriba
                    if vehiculo[0] == 1 and vadj[0] == 2:
                        return False
                    # Esta abajo
                    elif vehiculo[0] == filas and vadj[0] == (filas -1):
                        return False
                    else:
                        if vadj[0] == (vehiculo[0] - 1): 
                            for k in range(len(args)):
                                if k != i and k != j:
                                    if args[k][0] == vehiculo[0] + 1:
                                        return False
                        elif vadj[0] == vehiculo[0] + 1:
                            for k in range(len(args)):
                                if k!= i and k != j:
                                    if args[k][0] == vehiculo[0] -1:
                                        return False                         
    return True


def prioridad(vehiculo_i, vehiculo_j):
    if vehiculo_i[0] == vehiculo_j[0]:
        return vehiculo_i[1] > vehiculo_j[1]
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
    indice = 3
    while indice < len(lista_elec) - 1:
        lec = lista_elec[indice:indice + 5]
        indice += 5
        tupla = (int(lec[1]), int(lec[3]))
        dominio_electrico.append(tupla)
    return dominio_electrico


def calc_dominio_entero(columnas, filas):
    dominio_entero = []
    for row in range(filas):
        for col in range(columnas):
            pos = (row + 1, col + 1)
            dominio_entero.append(pos)
    return dominio_entero


if __name__ == "__main__":
    main(sys.argv[1])
