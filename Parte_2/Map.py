class Map:
	def __init__(self, tablero):
		self.mapa = []
		self.parking = []
		self.c = []
		self.nc = []
		self._inicializar_mapa(tablero)
		self._encuentra_todo()
		
	def _inicializar_mapa(self, tablero):
		for row in range(len(tablero)):
			lista = tablero[row].split(";")
			lista[-1] = lista[-1][0:-1]
			self.mapa.append(lista)
	
	def _encuentra_todo(self):
		for i in range(len(self.mapa)):
			for j in range(len(self.mapa[i])):
				casilla = self.mapa[i][j]
				if casilla == "P":
					self.parking = [i, j]
				elif casilla == "C":
					self.c.append(casilla)
				elif casilla == "N":
					self.nc.append(casilla)
					
	
	def __str__(self):
		string = ""
		for row in self.mapa:
			string += str(row)
			string += "\n"
		return string
					
