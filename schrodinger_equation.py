import numpy as np   # Import NumPy package which enables all the fun with algebra
from scipy.sparse import csc_matrix #package for working with csc matrices
import plotly.offline as py
from plotly import graph_objs as go

h = 1.054 * 10 ** -34 # Дж·с
e = 1.60217662 * 10 ** -19 # Кулон
m = 9.10938356 * 10 ** -31 # масса электрона


def potential_of_atom(x,y,z):
    """U(x,y,z) potential"""
    return 1/ np.sqrt(x**2 + y**2 + z**2)

def potential_pit(x,y,z):
    """U(x,y,z) potential"""
    if  x**2 <= 10 and y**2 <= 10 and z**2 <= 10:
        return 0
    else:
        return 100

def column(matrix, i):
    return [row[i] for row in matrix]

class SchorodingerSolver3D:
    d = 2  #grid step
    N = 6 #grid size
    k = 2 * m * d**2 / h**2 #normalization coeff

    def generateMatrix(self, potential):
        N = self.N
        d = self.d
        self.matrix_size = (N * 2) ** 3
        m = [[0 for i in range(self.matrix_size)] for j in range(self.matrix_size)]
        for i in range(2 * N):
            for j in range(2 * N):
                for k in range(2 * N):
                    line = i * (2 * N)**2 + j * (2 * N) + k
                    m[line][line] = potential((i - N + 0.5) * d, (j - N + 0.5) * d, (k - N + 0.5) * d) + 6
                    
                    if line - 1 >= 0:
                        m[line][line - 1] = -1
                    if line -  2 * N >= 0:
                        m[line][line - 2 * N] = -1
                    if line - (2 * N)**2 >= 0:
                        m[line][line - (2 * N)**2] = -1

                    if line + 1 < self.matrix_size:
                        m[line][line + 1] = -1
                    if line +  2 * N < self.matrix_size:
                        m[line][line + 2 * N] = -1
                    if line + (2 * N)**2 < self.matrix_size:
                        m[line][line + (2 * N)**2] = -1

        
        self.matrix = m
        self.λ, self.U = np.linalg.eigh(m)
        #print(self.λ)
    def __getPointByNumber(self, number):
        return [number // ((2 *self.N) ** 2) - self.N + 0.5,
            number % ((2 * self.N) ** 2) // (2 *self.N) - self.N + 0.5,
            number % (2 * self.N) - self.N + 0.5]

    def drawProbabilityDistribution(self, psi):
        avg_psi_square = (max(list(map(lambda x: x*x, psi))) - min(list(map(lambda x: x*x, psi))))/2
        
        points = []
        for i in range(len(psi)):
            if psi[i]**2 > avg_psi_square:
                points.append(i)

        x = [self.__getPointByNumber(num)[0] for num in points]
        y = [self.__getPointByNumber(num)[1] for num in points]
        z = [self.__getPointByNumber(num)[2] for num in points] 
        fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z,
                                    mode='markers')])
        py.plot(fig, filename='./elevations-3d-surface3.html')

ss = SchorodingerSolver3D()

ss.generateMatrix(potential_pit)
ss.drawProbabilityDistribution(ss.U[:,2])
print(ss.λ)
print(ss.U)
