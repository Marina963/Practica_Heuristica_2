class Map:
	def __init__(self, tablero):
		self.mapa = {}
		self.parking = []
		self.c = []
		self.nc = []
		self.h_cc = []
		self.h_nc = []
		if type(tablero) == list:
			self._inicializar_mapa(tablero)
		else:
			for i in tablero:
				self.mapa[i] = tablero[i].copy()
		self._encuentra_todo()
		
	def _inicializar_mapa(self, tablero):
		for row in range(len(tablero)):
			self.mapa[row] = {}
			for col in range(len(tablero[row])):
				self.mapa[row][col] = tablero[row][col]
	
	def _encuentra_todo(self):
		for i in range(len(self.mapa)):
			for j in range(len(self.mapa[i])):
				casilla = self.mapa[i][j]
				if casilla == "P":
					self.parking = [i, j]
				elif casilla == "C":
					self.c.append([i, j])
				elif casilla == "N":
					self.nc.append([i, j])
				elif casilla == "CC":
					self.h_cc.append([i, j])
				elif casilla == "CN":
					self.h_nc.append([i, j])

	def __str__(self):
		string = ""
		for row in self.mapa.keys():
			for col in self.mapa[row].keys():
				string += self.mapa[row][col] + "#"
			string += "\n"
		return string
					
