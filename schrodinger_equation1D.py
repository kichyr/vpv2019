import numpy as np   # Import NumPy package which enables all the fun with algebra
from scipy.sparse import csc_matrix #package for working with csc matrices
import plotly.offline as py
from plotly import graph_objs as go
import plotly.express as px


h = 1.054 * 10 ** -34 # Дж·с
e = 1.60217662 * 10 ** -19 # Кулон
m = 9.10938356 * 10 ** -31 # масса электрона


def potential_of_atom(x):
    """U(x,y,z) potential"""
    return 1/x

def potential_pit(x):
    """U(x,y,z) potential"""
    if  x**2 <= 400:
        return 0
    else:
        return 100

def column(matrix, i):
    return [row[i] for row in matrix]

class SchorodingerSolver3D:
    d = 1  #grid step
    N = 100 #grid size
    k = 2 * m * d**2 / h**2 #normalization coeff

    def generateMatrix(self, potential):
        N = self.N
        d = self.d
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

    def drawProbabilityDistribution(self, psi):        
        f_x = psi
        x = [self.__getPointByNumber(x) for x in range(self.matrix_size)]
        
        fig = go.Figure(data=go.Scatter(x=x, y=f_x, mode='markers'))
        
        py.plot(fig, filename='./elevations-1d-surface3.html')

ss = SchorodingerSolver3D()

ss.generateMatrix(potential_pit)
ss.drawProbabilityDistribution(ss.U[:,0])
print(len(ss.λ))
print(ss.λ)