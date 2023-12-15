from Constantes import *
import math
from Map import Map


class Ambulancia:
	def __init__(self, pos_inicial, plazas_c, plazas_nc, bateria, coste, predecesor_indice, tablero):
		#Parámetros que distinguen al estado
		self.pos = pos_inicial.copy()
		self.plazas_c = plazas_c.copy()
		self.plazas_nc = plazas_nc.copy()
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
		return str(self.pos) + " " + str(self.plazas_c) + " " + str(self.plazas_nc) + " " + str(self.mapa.c) + " " + str(self.mapa.nc) + " " + str(self.evaluacion) 

	def dist_manhattan(self, src, lista) -> int:
		"""Función que devuelve la distancia Manhattan mínima entre el estado y una lista de posiciones"""
		minimo = math.inf
		pos = []
		for i in range(len(lista)):
			dist = abs(int(src[0]) - int(lista[i][0])) + abs(int(src[1]) - int(lista[i][1]))
			if dist < minimo:
				minimo = dist
				pos = lista[i].copy()
		return minimo, pos
	
	def dist_euclidea(self, src, lista) -> int:
		"""Función que devuelve la distancia Euclidea mínima entre el estado y una lista de posiciones"""
		minimo = math.inf
		pos = []
		for i in range(len(lista)):
			dist = math.sqrt((int(src[0]) - int(lista[i][0]))**2 + (int(src[1]) - int(lista[i][1]))**2)
			if dist < minimo:
				minimo = dist
				pos = lista[i].copy()
		return minimo, pos

		
	def get_state(self) -> list:
		"""Función que devuelve el estado, usada para ver si el estado es final"""
		return [self.mapa.nc, self.mapa.c, self.pos, self.plazas_c, self.plazas_nc]

	def get_data(self) -> list:
		"""Función que proporciona información sobre el estado, usada para evitar repeticiones en la lista cerrada"""
		return (self.pos, self.plazas_c, self.bateria, self.plazas_nc, self.mapa.c, self.mapa.nc)
	
	def get_hashable_data(self, num_cols) -> list:
		hashable = ""
		hashable = str(self.pos[0]*num_cols + self.pos[1]) + "-"
		for i in self.plazas_c:
			hashable += i
		hashable += "-"
		for i in self.plazas_nc:
			hashable += i
		hashable += "-"
		hashable += str(self.bateria)
		hashable += "-"
		for i in self.mapa.c:
			hashable += str(i[0]*num_cols + i[1])
		hashable += "-"
		for i in self.mapa.nc:
			hashable += str(i[0]*num_cols + i[1])
		hashable += "-"
		return hashable
	
	#Funciones principales
	def mover(self, operacion: int, num_h: int) -> bool:
		"""Función que evalúa las precondiciones y ejecuta los efectos si procede"""
		if not self._precondiciones(operacion):
			return False
		self._efectos(operacion, num_h)
		return True

	def _h_1(self) -> int:
		heuristica = 0
		nodos_c = self.mapa.c.copy()
		nodos_nc = self.mapa.nc.copy()
		plazas_c, plazas_nc = self.plazas_c.copy(), self.plazas_nc.copy()
		pos = self.pos.copy()
		while 1:
			minimo_nc, minimo_c, minimo_hc, minimo_hn = math.inf, math.inf, math.inf, math.inf
			if len(nodos_nc) > 0 and len(plazas_nc) < capacidad_max[0] and (len(plazas_c) == 0 or plazas_c[0] == "nc"):
				minimo_nc, pos_nc = self.dist_manhattan(pos, nodos_nc)
			if len(nodos_c) > 0 and len(plazas_c) < capacidad_max[1] and (len(plazas_c) == 0 or plazas_c[0] == "c"):
				minimo_c, pos_c = self.dist_manhattan(pos, nodos_c)
			if len(plazas_c) > 0 and len(self.mapa.h_cc) > 0 and plazas_c[0] == "c":
				minimo_hc, pos_hc = self.dist_manhattan(pos, self.mapa.h_cc)  	
			if len(plazas_nc) > 0 and len(self.mapa.h_nc) > 0 and (len(plazas_c) == 0 or plazas_c[0] == "nc"):
				minimo_hn, pos_hn = self.dist_manhattan(pos, self.mapa.h_nc)
			
			if len(plazas_c) == 0 and len(plazas_nc) == 0 and len(nodos_c) == 0 and len(nodos_nc) == 0:
				heuristica += self.dist_manhattan(pos, [self.mapa.parking])[0]	
				return heuristica
			if not math.isinf(minimo_nc):
				nodos_nc.remove(pos_nc)
				pos = pos_nc
				if len(plazas_nc) < capacidad_max[0]:
					plazas_nc += ["nc"]
				elif len(plazas_c) == 0 or plazas_c[0] == "nc":
					plazas_c += ["c"]
			elif not math.isinf(minimo_c):
				nodos_c.remove(pos_c)
				pos = pos_c
				plazas_c += ["c"]
			elif not math.isinf(minimo_hc):
				if len(plazas_c) > 0 and plazas_c[0] == "c":
					plazas_c.clear()
				pos = pos_hc
			elif not math.isinf(minimo_hn):
				if len(plazas_nc) > 0:
					plazas_nc.clear()
				if len(plazas_c) > 0 and plazas_c[0] == "nc":
					plazas_c.clear()
				pos = pos_hn.copy()
			minimo = min(minimo_nc, minimo_c, minimo_hc, minimo_hn)
			heuristica += minimo

			
	"""def _h_1(self) -> int:
		#Función heurística 1 - Manhattan
		minimo = math.inf
		if len(self.mapa.nc) > 0 and ((len(self.plazas_c) == 0 and len(self.plazas_nc) < capacidad_max[0]) or (self.plazas_c[0] == "nc" and len(self.plazas_c) < capacidad_max[1])):
			minimo = self.dist_manhattan(self.pos, self.mapa.nc)
		elif len(self.mapa.c) > 0 and (len(self.plazas_c) == 0 or self.plazas_c[0] == "c") and len(self.plazas_c) < capacidad_max[1]:
			minimo = self.dist_manhattan(self.pos, self.mapa.c)
		elif len(self.plazas_c) > 0 and self.plazas_c[0] == "c":
			minimo = self.dist_manhattan(self.pos, self.mapa.h_cc)
		elif len(self.plazas_nc) > 0 or (len(self.plazas_c) > 0 and self.plazas_c[0] == "nc"):
			minimo = self.dist_manhattan(self.pos, self.mapa.h_nc)
			
		if (len(self.plazas_nc) == 0 and len(self.mapa.nc) == 0 and len(self.plazas_c) == 0 and len(self.mapa.c) == 0) or self.bateria < minimo:
			minimo = self.dist_manhattan(self.pos, [self.mapa.parking])
		try:
		 	coste = int(self.casilla)
		 	return minimo + coste - 1
		except:
			return minimo 
	"""
	def _h_2(self) -> int:
		"""Función heurística 2 - Euclidea"""
		if len(self.mapa.nc) != 0 and capacidad_max[0] > len(self.plazas_nc):
			minimo = self.dist_euclidea(self.pos, self.mapa.nc)
		elif len(self.mapa.c) != 0 and capacidad_max[1] > len(self.plazas_c):
			min_1 = self.dist_euclidea(self.pos, self.mapa.c)
			min_2 = math.inf
			if len(self.plazas_c) == 0 and len(self.plazas_nc) > 0:
				min_2 = self.dist_euclidea(self.pos, self.mapa.h_nc)
			minimo = min(min_1, min_2)
		elif (capacidad_max[1] == len(self.plazas_c) and self.plazas_c[0] == "c") or (len(self.mapa.c) == 0 and len(self.plazas_c) > 0 and self.plazas_c[0]  == "c"):
			minimo = self.dist_euclidea(self.pos, self.mapa.h_cc)
		elif capacidad_max[0] == len(self.plazas_nc) or (len(self.mapa.nc) == 0 and len(self.plazas_nc) > 0):
			minimo = self.dist_euclidea(self.pos, self.mapa.h_nc)
		else:
			minimo = self.dist_euclidea(self.pos, [self.mapa.parking]) - self.coste
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


	def _efectos(self, operacion, num_h):
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
				if len(self.plazas_nc) < capacidad_max[0] and (len(self.plazas_c) == 0 or self.plazas_c[0] != "c"):
					self.plazas_nc.append("nc")
					self.mapa.nc.remove([casilla_pos[0], casilla_pos[1]])
					self.mapa.mapa[casilla_pos[0]][casilla_pos[1]] = "1"
				elif ("c" not in self.plazas_c and len(self.plazas_c) < capacidad_max[1]):
					self.plazas_c.append("nc")
					self.mapa.nc.remove([casilla_pos[0], casilla_pos[1]])
					self.mapa.mapa[casilla_pos[0]][casilla_pos[1]] = "1"
			case "C":
				if (len(self.plazas_c) < capacidad_max[1] ) and "nc" not in self.plazas_c:
						self.plazas_c.append("c")
						self.mapa.c.remove([casilla_pos[0], casilla_pos[1]])
						self.mapa.mapa[casilla_pos[0]][casilla_pos[1]] = "1"
			case "CC":
				self.plazas_c.clear()
			case "CN":
				if len(self.plazas_c) > 0 and "nc" in self.plazas_c:
					self.plazas_c.clear()
				if len(self.plazas_c) == 0:
					self.plazas_nc.clear()
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

