import sys
from Ambulance import Ambulancia
from Map import Map
from constantes import *


def main(input_file, num_h):
	#Apertura de fichero
	with open(input_file) as file:
		tablero = file.readlines()
	
	#Creacion del mapa y de la ambulancia
	mapa = Map(tablero)
	nodo_inicial = Ambulancia(mapa.parking, [], [], bateria_max, [0, 0], 0, None,  mapa.mapa)
	nodo_final = Ambulancia(mapa.parking, [], [], bateria_max, [len(mapa.c), len(mapa.nc)], 0,None, mapa.mapa)

	camino = astar(nodo_inicial, nodo_final, num_h, mapa)
	if camino != False:
		print("El camino es: ")
		for i in range(len(camino)):
			print(camino[i])
	else:
		print("No existe camino")
	return


def astar(nodo_inicial, nodo_final, num_h, mapa):
	lista_abierta = [nodo_inicial]
	lista_cerrada = []
	exito = False
	estado_final = nodo_final.get_state()
	while len(lista_abierta) > 0 and not exito:
		nodo = lista_abierta.pop(0)
		estado = nodo.get_state()
		if estado[0] == estado_final[0] and estado[1] == estado_final[1] and estado[2] == estado_final[2]:
			exito = True
		else:
			lista_cerrada.append(nodo)
			conjunto_s = generar_sucesores(nodo, num_h, mapa, len(lista_cerrada) - 1)
			for i in range(len(conjunto_s)):
				s = conjunto_s[i]
				data_s = s.get_data()
				if not in_lista_cerrada(lista_cerrada, data_s):
					pos = in_lista_abierta(lista_abierta, data_s)
					if pos != -1:
						if s.evaluacion < lista_abierta[pos].evaluacion:
							lista_abierta[pos] = s
					else:
						lista_abierta.append(s)
			sorted(lista_abierta, key=lambda nodo: nodo.evaluacion)
	if exito:
		if len(lista_cerrada) == 0:
			return nodo_inicial.pos
		predecesor = nodo.predecesor
		camino = [nodo.pos]
		while predecesor:
			camino.insert(0, (lista_cerrada[predecesor].pos, lista_cerrada[predecesor].ocupacion_hospitales))
			predecesor = lista_cerrada[predecesor].predecesor
		camino.insert(0, (lista_cerrada[0].pos))
		return camino
	return False
								

def in_lista_cerrada(lista, data_s):
	for dato in lista:
		iguales = True
		data_d = dato.get_data()
		for i in range(len(data_s)):
			dato_s = data_s[i]
			dato_d = data_d[i]
			if type(dato_s) == int:
				if dato_s != dato_d:
					iguales = False
			else:
				for j in range(len(dato_s)):
					if len(dato_s) != len(dato_d) or dato_s[j] != dato_d[j]:
						iguales = False
		if iguales:
			return True
	return False


def in_lista_abierta(lista, data_s):
	for k in range(len(lista)):
		iguales = k
		data_d = lista[k].get_data()
		for i in range(len(data_s)):
			dato_s = data_s[i]
			dato_d = data_d[i]
			if type(dato_s) == int:
				if dato_s != dato_d:
					iguales = -1
			else:
				for j in range(len(dato_s)):
					if len(dato_s) != len(dato_d) or dato_s[j] != dato_d[j]:
						iguales = -1
		if iguales != -1:
			return iguales
	return -1


def generar_sucesores(nodo, num_h, mapa, predecesor):
	lista_sucesores = []
	for i in range(4):
		sucesor = Ambulancia(nodo.pos, nodo.plazas_c, nodo.plazas_nc, nodo.bateria, nodo.ocupacion_hospitales, nodo.coste,predecesor, nodo.tablero)
		booleano = sucesor.mover(i, num_h, len(mapa.nc), len(mapa.c))
		if booleano:
			lista_sucesores.append(sucesor)
	return lista_sucesores


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
		except:
			print("num_h must be a number.")
