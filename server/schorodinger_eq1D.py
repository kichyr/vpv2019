import numpy as np   # Import NumPy package which enables all the fun with algebra
from decimal import *

ħ = 6.582 * 10 ** -16 # 
e = 1.60217662 * 10 ** -19 # Кулон
electron_mass = 9.10938356 * 10 ** -31 # масса электрона


class SchorodingerSolver1D:
    d = 1
    N = 200 #grid size
    k = 2 * electron_mass * d**2 / (ħ**2) #normalization coeff

    def generateMatrix(self, potential, sys_size):
        global h, e, electron_mass
        d = sys_size / self.N
        self.d = d
        self.k = 2 * electron_mass * d**2 / ħ**2 
        N = self.N
        self.matrix_size = (N * 2)
        m = [[0 for i in range(self.matrix_size)] for j in range(self.matrix_size)]
        for i in range(2 * N):
            m[i][i] = self.k * potential((i - N + 0.5) * self.d) + 2
            
            if i - 1 >= 0:
                m[i][i - 1] = -1

            if i + 1 < self.matrix_size:
                m[i][i + 1] = -1
        
        self.matrix = m
        self.λ, self.U = np.linalg.eig(m)

        self.indexes = list(range(len(self.λ)))
        self.λ,self.indexes = zip(*sorted(zip(self.λ, self.indexes)))
        self.indexes = list(self.indexes)

    def __getPointByNumber(self, number):
        return number - self.N + 0.5


    def get_output_data(self):
        phi = []
        x = []
        for index in self.indexes:
            phi.append(list(self.U[:,index]))
        for i in range(self.matrix_size):
            x.append(self.__getPointByNumber(i) * self.d)
        return {"E": list(map(lambda x: "{:.2E}".format(Decimal(str(x / self.k))), list(self.λ))),
                "phi": phi,
                "x": x,
                "E_not_formated": list(map(lambda x: x / self.k, list(self.λ)))}