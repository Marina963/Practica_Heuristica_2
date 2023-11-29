import random

from constraint import *
import sys
from vehiculos import Vehiculos

global ad
global filas
global columnas
ad = False

def set_ad(value):
    global ad
    ad = value
    
def set_filas(value):
    global filas
    filas = value
    
def set_columnas(value):
    global columnas
    columnas = value

def main(file):
    with open(file, "r") as f:
        lectura = f.readlines()
    
    num_rows = lectura[0].index("x")
    set_filas(int(lectura[0][0:num_rows]))
    num_cols = lectura[0].index("\n")
    set_columnas(int(lectura[0][num_rows + 1:num_cols]))
    
    dominio_entero = calc_dominio_entero(columnas, filas)
    dominio_electrico = calc_dominio_electrico(lectura[1])
    if (isinstance(dominio_electrico, int)): return -1
    dominio_no_electrico = calc_dominio_no_electrico(dominio_electrico, dominio_entero)
    
    variables = crear_variables(lectura)
    
    problem = Problem()
    for v in variables:
        if v.freezer == "C":
            problem.addVariable(str(v), dominio_electrico)
        else:
            problem.addVariable(str(v), dominio_no_electrico)

    problem.addConstraint(AllDifferentConstraint())
    for i in variables:
        for j in variables:
            if i.id != j.id:
                if i.type == "TSU" and j.type == "TNU":
                    problem.addConstraint(prioridad, (str(i), str(j)))
    problem.addConstraint(adyacencia, problem._variables)
                    
    sol = problem.getSolutions()
    sols = []
    for i in range(min(10, len(sol))):
        num = random.randint(0, len(sol) - 1)
        sols.append(sol[num])
    escr_salida(len(sol), sols, file)


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

def adyacencia(*variables):
    for vehiculo in variables:
        for vadj in variables:
            if vehiculo != vadj:
                if vehiculo[1] == vadj[1]:
                    #Esta arriba
                    if vehiculo[0] == 1 and vadj[0] == 2:
                        return False
                    #Esta abajo
                    elif vehiculo[0] == filas and vadj[0] == (filas - 1):
                        return False
                    else:
                        if vadj[0] == (vehiculo[0] - 1):
                            for vadj2 in variables:
                                if vadj2[1] == vadj[1] and vadj2[0] == (vehiculo[0] + 1):
                                    return False
                        elif vadj[0] == vehiculo[0] + 1:
                            for vadj2 in variables:
                                if vadj2[1] == vadj[1] and vadj2[0] == (vehiculo[0] - 1):
                                    return False
    return True

def prioridad(vehiculo_i, vehiculo_j):
    if vehiculo_i[0] == vehiculo_j[0]:
        return vehiculo_i[1] > vehiculo_j[1]
    return True

def crear_variables(lectura):
	lista = []
	for i in range(2, len(lectura)):
	    index = lectura[i].index("-")
	    v = Vehiculos(lectura[i][0:index], lectura[i][index+1:index+4], lectura[i][index+5])
	    lista.append(v)
	return lista

def calc_dominio_entero(columnas, filas):
	dominio_entero = []
	for row in range(filas):
	    for col in range(columnas):
	        pos = (row + 1, col + 1)
	        dominio_entero.append(pos)
	return dominio_entero

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
	    opening = lista_elec.index("(", indice)
	    closing = lista_elec.index(")", indice)
	    lec = lista_elec[opening: closing]
	    sep = lec.index(",")
	    tupla = (int(lec[1:sep]), int(lec[sep + 1:]))
	    if tupla[0] > filas:
	        print("Row out of index. " + str(filas) + " is max, but " + str(tupla[0]) + " was given.")
	        return -1
	    if tupla[1] > columnas:
	        print("Column out of index. " + str(columnas) + " is max, but " + str(tupla[1]) + " was given.")
	        return -1
	    dominio_electrico.append(tupla)
	    indice += len(lec) + 1
	return dominio_electrico

if __name__ == "__main__":
    if len(sys.argv) < 2:
       print("File not specified.")
    elif len(sys.argv) > 2:
       print("Too many arguments, main.py needs 2 but " + str(len(sys.argv)) + " were given.")
    else:
       main(sys.argv[1])
    
