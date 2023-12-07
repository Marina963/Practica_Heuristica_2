from constantes import *

class Ambulancia:
	def __init__(self, pos_inicial, plazas_c, plazas_nc, bateria, ocupacion_hospitales, coste, num_h, predecesor_indice):
		self.pos = pos_inicial.copy()
		self.plazas_c = plazas_c.copy()
		self.plazas_nc = plazas_nc.copy()
		#Primero c y luego n
		self.ocupacion_hospitales = ocupacion_hospitales.copy()
		self.bateria = bateria
		self.coste = coste
		self.heuristica = 0
		self.evaluacion = 0
		self.predecesor = predecesor_indice
	
	def __str__(self):
		return str(self.pos) 
	
	def mover(self, tablero, operacion, num_h):
		if self._precondiciones(tablero, operacion) == False:
			return False
		self._efectos(tablero, operacion, num_h)
		return True
		
	def _h_1(self):
		return 1
		
	def _h_2(self):
		return 2
	
	def get_state(self):
		return [self.pos, self.ocupacion_hospitales[0], self.ocupacion_hospitales[1]]	
	
	def get_data(self):
		return [self.pos, self.ocupacion_hospitales, self.plazas_c, self.plazas_nc]
	
	def _precondiciones(self, tablero, operacion):	
		"""Precondiciones"""
		match operacion:
			#Abajo
			case 0:
				limite = self.pos[0] + 1
				if (limite > len(tablero.mapa) - 1):
					return False
				casilla = tablero.mapa[self.pos[0] +1][self.pos[1]]
			#Arriba
			case 1:
				limite = self.pos[0] -1
				if (limite < 0):
					return False
				casilla = tablero.mapa[self.pos[0]-1][self.pos[1]]
			#Izquierda
			case 2:
				limite = self.pos[1] - 1
				if (limite < 0):
					return False
				casilla = tablero.mapa[self.pos[0]][self.pos[1]-1]
			#Derecha
			case 3:
				limite = self.pos[1] + 1
				if (limite > len(tablero.mapa[0]) -1):
					return False
				casilla = tablero.mapa[self.pos[0]][self.pos[1] +1]
			case _:
				return False
		#Si no tiene bateria o no puede transitar
		if (self.bateria == 0 or casilla == "X"):
			return False
		#Calcula la batería
		try:
			bateria_gastada = int(casilla)
		except:
			bateria_gastada = 1
		if (self.bateria - bateria_gastada < 0):
			return False
		return casilla

	def _efectos(self, tablero, operacion, num_h):
		"""Efectos"""
		#Mira que tipo de casilla es a la que se mueve
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
		casilla = tablero.mapa[casilla_pos[0]][casilla_pos[1]]
		try:
			bateria_gastada = int(casilla)
		except:
			bateria_gastada = 1
		match casilla:
			case "N":
				print(self.pos, self.plazas_nc, operacion)
				if len(self.plazas_nc) < capacidad_max[0]:
					self.plazas_nc.append("nc")
					tablero.mapa[casilla_pos[0]][casilla_pos[1]] = "1"
				elif len(self.plazas_c) == 0 or ("c" not in self.plazas_c and len(self.plazas_c) < capacidad_max[1]) or len(self.ocupacion_hospitales) == len(tablero.c):
					self.plazas_c.append("nc")
					tablero.mapa[casilla_pos[0]][casilla_pos[1]] = "1"
			case "C":
				if len(self.plazas_c) < capacidad_max[1] and "nc" not in self.plazas_c:
					if self.plazas_nc == capacidad_max[0] or len(tablero.nc) == self.ocupacion_hospitales[1] + len(self.plazas_nc): 
						self.plazas_c.append("c")
						tablero.mapa[casilla_pos[0]][casilla_pos[1]] = "1"
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
		if casilla != "P":
			self.bateria -= bateria_gastada
		self.coste += bateria_gastada
		#Calcular la h(n)
		if num_h == 1:
			self.heuristica = self._h_1()
		else:
			self.heuristica = self._h_2() 
		#Calcular la f(n)
		self.coste += bateria_gastada
		self.evaluacion = self.heuristica + self.coste
		#Cambiar la posicion
