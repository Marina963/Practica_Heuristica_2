import math
import sys
from Ambulance import Ambulancia
from Map import Map
from Constantes import *
from collections import Counter
import time


def main(input_file, num_h):
    #Apertura de fichero
    with open(input_file) as file:
        tablero_leido = file.readlines()
    
    tablero = []
    for i in range(len(tablero_leido)):
        linea = tablero_leido[i].split(";")
        linea[len(linea) -1] = linea[len(linea) -1][0:-1]
        tablero.append(linea)
        
    
    #Creacion del mapa y de la ambulancia
    mapa = Map(tablero)
  
    nodo_inicial = Ambulancia(mapa.parking, [], [], bateria_max, 0, None,  mapa.mapa)
    nodo_final = Ambulancia(mapa.parking, [], [], bateria_max, 0,None, mapa.mapa)
    nodo_final.mapa.c, nodo_final.mapa.nc = [], [] 
     
    inicio = time.time()
    salida = astar(nodo_inicial, nodo_final, num_h, mapa)
    final = time.time()
    
    if salida == False:
        print("No existe camino")
        return False
    
    escribir_salida(salida[0], num_h, input_file)
    escribir_estadisticas(salida, round(final - inicio, 2), input_file, num_h)
    return True


def astar(nodo_inicial, nodo_final, num_h, mapa):
    """Función que se encarga de aplicar el algoritmo A*"""
    num_cols = len(mapa.mapa[0])
    lista_abierta = {nodo_inicial.get_hashable_data(num_cols): nodo_inicial}
    lista_cerrada = {}
    exito = False
    estado_final = nodo_final.get_state()
    
    global contador
    contador = 0
 
    while not exito and len(lista_abierta) >  0:
        nodo_hasheado = next(iter(lista_abierta))
        nodo = lista_abierta.pop(nodo_hasheado)
        estado = nodo.get_state()
        if estado[0] == estado_final[0] and estado[1] == estado_final[1] and estado[2] == estado_final[2] and estado[3] == estado_final[3] and estado[4] == estado_final[4]:
            exito = True
        else:
            lista_cerrada[nodo_hasheado] = nodo
            conjunto_s = generar_sucesores(nodo, num_h, nodo_hasheado)
            for s in conjunto_s:
                data_s = s.get_hashable_data(num_cols)
                if not in_lista_cerrada(lista_cerrada, data_s):
                    if in_lista_abierta(lista_abierta, s, data_s):
                        lista_abierta = dict(sorted(lista_abierta.items(), key=lambda nodo: nodo[1].evaluacion))
    print(contador)
    if exito:
        if len(lista_cerrada) == 0:
            return ([(nodo_inicial.pos, "P", 50)], 0, 0)
        predecesor = nodo.predecesor
        camino = [(nodo.pos, nodo.casilla, nodo.bateria)]
        while predecesor:
            nodo_camino = lista_cerrada[predecesor]
            camino.insert(0, ((nodo_camino.pos, nodo_camino.casilla, nodo_camino.bateria)))
            predecesor = nodo_camino.predecesor
        camino.insert(0, (nodo.pos, nodo.casilla, nodo.bateria))
        return (camino, len(lista_cerrada), nodo.coste)
        
    #Si no hay solución, devuelve False   
    return False

def in_lista_cerrada(lista, data_s):
	try:
		aux = lista[data_s]
		return True
	except KeyError:
		return False


def in_lista_abierta(lista, sucesor, data_s):
    global contador
    try:
        aux = lista[data_s]
        if sucesor.evaluacion < aux.evaluacion:
            lista[data_s] = sucesor
            return True
        contador += 1
        return False
    except:
        lista[data_s] = sucesor
        return True


def generar_sucesores(nodo, num_h, predecesor):
    lista_sucesores = []
    for i in range(4):
        sucesor = Ambulancia(nodo.pos, nodo.plazas_c, nodo.plazas_nc, nodo.bateria, nodo.coste, predecesor, nodo.mapa.mapa)
        booleano = sucesor.mover(i, num_h)
        if booleano:
            lista_sucesores.append(sucesor)
    return lista_sucesores

def escribir_salida(camino, num_h, input_file):
    input_name = input_file 
    
    if len(camino) > 1:
        camino.pop(1)
    try:
        index_of_directory = input_name.index("/")
        while 1:
            input_name = input_name[index_of_directory +1: -1]
            index_of_directory = input_name.index("/")
    except ValueError:
        index_of_dot = input_name.index(".")      
    name = input_name[0:index_of_dot] + "-" + str(num_h) + ".output"
    name = "ASTAR-test/" + name
      
    with open(name, "w") as file:
        for path in camino:
            linea = str(tuple(path[0])) + ":" + path[1] + ":" + str(path[2]) + "\n"
            file.write(linea)
    return

def escribir_estadisticas(salida, tiempo, input_file, num_h):
    camino = salida[0]
    nodos = salida[1]
    input_name = input_file
    
    try:
        index_of_directory = input_name.index("/")
        while 1:
            input_name = input_name[index_of_directory + 1:-1] 
            index_of_directory = input_name.index("/")
    except ValueError:            
        index_of_dot = input_name.index(".")
    name = input_name[0:index_of_dot] + "-" + str(num_h) + ".stat" 
    name = "ASTAR-test/" + name
   
    with open(name, "w") as file:
        file.write("Tiempo total: " + str(tiempo) + "\n")
        file.write("Coste total: " + str(salida[2]) + "\n")
        file.write("Longitud del plan: " + str(len(camino) -1) + "\n")
        file.write("Nodos expandidos: " + str(nodos) + "\n")
    return
    
if __name__=="__main__":
    if len(sys.argv) != 3:
        print("Main takes 2 arguments, but " + str(len(sys.argv) - 1) + " were given.")
    else:
        try:
            arg_2 = int(sys.argv[2])
            if arg_2 == 1 or arg_2 == 2:
                main(sys.argv[1], arg_2)
            else:
                print("num_h takes values 1 or 2.")
        except ValueError:
            print("num_h must be a number.")
