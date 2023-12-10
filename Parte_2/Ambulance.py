from constantes import *
import math
from Map import Map


class Ambulancia:
	def __init__(self, pos_inicial, plazas_c, plazas_nc, bateria, ocupacion_hospitales, coste, predecesor_indice, tablero):
		#Parámetros que distinguen al estado
		self.pos = pos_inicial.copy()
		self.plazas_c = plazas_c.copy()
		self.plazas_nc = plazas_nc.copy()
		#Primero c y luego n
		self.ocupacion_hospitales = ocupacion_hospitales.copy()
		#Parámetros relacionados con el coste y la heurística
		self.bateria = bateria
		self.coste = coste
		self.heuristica = 0
		self.evaluacion = 0
		#Parámetros relacionados con el estado del mapa
		self.predecesor = predecesor_indice
		self.mapa = Map(tablero)
		self.casilla = ""

	#Funciones auxiliares
	def __str__(self) -> str:
		"""Función auxiliar que permite escribir una ambulancia"""
		return str(self.pos) + " " + str(self.plazas_c) + " " + str(self.plazas_nc) + " " + str(self.ocupacion_hospitales) + " " + str(self.mapa.c) + " " + str(self.mapa.nc) + " " + str(self.evaluacion) 

	def dist_manhattan(self, lista) -> int:
		"""Función que devuelve la distancia Manhattan mínima entre el estado y una lista de posiciones"""
		mininimo = math.inf
		i = 0
		while i < len(lista):
			dist = abs(int(self.pos[0]) - int(lista[i][0])) + abs(int(self.pos[1]) - int(lista[i][1]))
			if dist < mininimo:
				mininimo = dist
			i += 1
		return mininimo
	
	def dist_euclidea(self, lista) -> int:
		"""Función que devuelve la distancia Euclidea mínima entre el estado y una lista de posiciones"""
		mininimo = math.inf
		i = 0
		while i < len(lista):
			dist = math.sqrt((int(self.pos[0]) - int(lista[i][0]))**2 + (int(self.pos[1]) - int(lista[i][1]))**2)
			if dist < mininimo:
				mininimo = dist
			i += 1
		return mininimo

		
	def get_state(self) -> list:
		"""Función que devuelve el estado, usada para ver si el estado es final"""
		return [self.pos, self.ocupacion_hospitales[0], self.ocupacion_hospitales[1]]

	def get_data(self) -> list:
		"""Función que proporciona información sobre el estado, usada para evitar repeticiones en la lista cerrada"""
		return [self.pos, self.ocupacion_hospitales, self.plazas_c, self.plazas_nc]
		
	#Funciones principales
	def mover(self, operacion: int, num_h: int, nc: int, c: int) -> bool:
		"""Función que evalúa las precondiciones y ejecuta los efectos si procede"""
		if not self._precondiciones(operacion):
			return False
		self._efectos(operacion, num_h, nc, c)
		return True

	def _h_1(self) -> int:
		"""Función heurística 1 - Manhattan"""
		if len(self.mapa.nc) != 0 and capacidad_max[0] > len(self.plazas_nc):
			minimo = self.dist_manhattan(self.mapa.nc)
		elif len(self.mapa.c) != 0 and capacidad_max[1] > len(self.plazas_c):
			min_1 = self.dist_manhattan(self.mapa.c)
			min_2 = math.inf
			if len(self.plazas_nc) > 0:
				min_2 = self.dist_manhattan(self.mapa.nc)
			minimo = min(min_1, min_2)
		elif capacidad_max[1] == len(self.plazas_c) or (len(self.mapa.c) == 0 and len(self.plazas_c) > 0):
			minimo = self.dist_manhattan(self.mapa.h_cc)
		elif capacidad_max[0] == len(self.plazas_nc) or (len(self.mapa.nc) == 0 and len(self.plazas_nc) > 0):
			minimo = self.dist_manhattan(self.mapa.h_nc)
		else:
			minimo = self.dist_manhattan([self.mapa.parking])
		return minimo

	def _h_2(self) -> int:
		"""Función heurística 2 - Euclidea"""
		if len(self.mapa.nc) != 0 and capacidad_max[0] > len(self.plazas_nc):
			minimo = self.dist_euclidea(self.mapa.nc)
		elif len(self.mapa.c) != 0 and capacidad_max[1] > len(self.plazas_c):
			min_1 = self.dist_euclidea(self.mapa.c)
			min_2 = math.inf
			if len(self.plazas_nc) > 0:
				min_2 = self.dist_euclidea(self.mapa.nc)
			minimo = min(min_1, min_2)
		elif capacidad_max[1] == len(self.plazas_c) or (len(self.mapa.c) == 0 and len(self.plazas_c) > 0):
			minimo = self.dist_euclidea(self.mapa.h_cc)
		elif capacidad_max[0] == len(self.plazas_nc) or (len(self.mapa.nc) == 0 and len(self.plazas_nc) > 0):
			minimo = self.dist_euclidea(self.mapa.h_nc)
		else:
			minimo = self.dist_euclidea([self.mapa.parking])
		return minimo

	
	def _precondiciones(self, operacion: int) -> bool:
		"""Precondiciones"""
		#Check de que la casilla a la que se mueve el estado sea una casilla válida
		match operacion:
			#Abajo
			case 0:
				limite = self.pos[0] + 1
				if limite > len(self.mapa.mapa) - 1:
					return False
				self.casilla = self.mapa.mapa[self.pos[0] +1][self.pos[1]]
			#Arriba
			case 1:
				limite = self.pos[0] - 1
				if (limite < 0):
					return False
				self.casilla = self.mapa.mapa[self.pos[0]-1][self.pos[1]]
			#Izquierda
			case 2:
				limite = self.pos[1] - 1
				if (limite < 0):
					return False
				self.casilla = self.mapa.mapa[self.pos[0]][self.pos[1]-1]
			#Derecha
			case 3:
				limite = self.pos[1] + 1
				if limite > len(self.mapa.mapa[0]) - 1:
					return False
				self.casilla = self.mapa.mapa[self.pos[0]][self.pos[1] +1]
			case _:
				return False
				
		#Si no tiene bateria o no puede transitar
		if self.bateria == 0 or self.casilla == "X":
			return False
		
		#Calcula la batería que va a gastar
		try:
			bateria_gastada = int(self.casilla)
		except:
			bateria_gastada = 1
		if self.bateria - bateria_gastada < 0:
			return False
		return True


	def _efectos(self, operacion, num_h,nc, c):
		"""Efectos"""
		#Mueve la ambulancia
		match operacion:
			case 0:
				self.pos[0] += 1
			case 1:
				self.pos[0] -= 1
			case 2:
				self.pos[1] -= 1
			case 3:
				self.pos[1] += 1
		casilla_pos = [self.pos[0], self.pos[1]]
		
		#Calcula la batería gastada
		try:
			bateria_gastada = int(self.casilla)
		except:
			bateria_gastada = 1
		self.bateria -= bateria_gastada
		
		#Mira que tipo de casilla es a la que se mueve
		match self.casilla:
			case "N":
				if len(self.plazas_nc) < capacidad_max[0]:
					self.plazas_nc.append("nc")
					self.mapa.mapa[casilla_pos[0]][casilla_pos[1]] = "1"
				elif len(self.plazas_c) == 0 or ("c" not in self.plazas_c and len(self.plazas_c) < capacidad_max[1]) or len(self.ocupacion_hospitales) == c:
					self.plazas_c.append("nc")
					self.mapa.mapa[casilla_pos[0]][casilla_pos[1]] = "1"
			case "C":
				if (len(self.plazas_c) < capacidad_max[1] ) and "nc" not in self.plazas_c:
					if self.plazas_nc == capacidad_max[0] or nc == self.ocupacion_hospitales[1] + len(self.plazas_nc):
						self.plazas_c.append("c")
						self.mapa.mapa[casilla_pos[0]][casilla_pos[1]] = "1"
			case "CC":
				while len(self.plazas_c) != 0:
					self.plazas_c.pop(0)
					self.ocupacion_hospitales[0] += 1
			case "CN":
				if len(self.plazas_c) > 0 and "nc" in self.plazas_c:
					while len(self.plazas_c) != 0:
						self.plazas_c.pop(0)
						self.ocupacion_hospitales[1] += 1
				if len(self.plazas_c) == 0:
					while len(self.plazas_nc) != 0:
						self.plazas_nc.pop(0)
						self.ocupacion_hospitales[1] += 1
			case "P":
				self.bateria = bateria_max
		
		#Calcular la h(n)
		if num_h == 1:
			self.heuristica = self._h_1()
		else:
			self.heuristica = self._h_2()
			
		#Calcular la f(n)
		self.coste += bateria_gastada
		self.evaluacion = self.heuristica + self.coste

