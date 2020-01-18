import numpy as np   # Import NumPy package which enables all the fun with algebra
from decimal import *

h = 1.054 * 10 ** -34 # Дж·с
e = 1.60217662 * 10 ** -19 # Кулон
electron_mass = 9.10938356 * 10 ** -31 # масса электрона


class SchorodingerSolver1D:
    d = 1
    N = 100 #grid size
    k = 2 * electron_mass * d**2 / h**2 #normalization coeff

    def generateMatrix(self, potential, d):
        global h, e, electron_mass
        d = d / self.N
        print("+++++++++++++++")
        print(d)
        self.d = d
        self.k = 2 * electron_mass * d**2 / h**2 
        N = self.N
        self.matrix_size = (N * 2)
        m = [[0 for i in range(self.matrix_size)] for j in range(self.matrix_size)]
        for i in range(2 * N):
            m[i][i] = potential((i - N + 0.5) * d) + 6
            
            if i - 1 >= 0:
                m[i][i - 1] = -1

            if i + 1 < self.matrix_size:
                m[i][i + 1] = -1
        
        self.matrix = m
        self.λ, self.U = np.linalg.eigh(m)

    def __getPointByNumber(self, number):
        return number - self.N + 0.5


    def get_output_data(self):
        phi = []
        x = []
        for i in range(self.matrix_size):
            phi.append(list(self.U[:,i]))
            x.append(self.__getPointByNumber(i) * self.d)
        return {"E": list(map(lambda x: "{:.2E}".format(Decimal(str(x))), list(self.λ))),
                "phi": phi,
                "x": x}