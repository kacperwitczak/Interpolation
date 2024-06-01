import math
import numpy as np

def linspace(a, b, n):
    step = (b - a) / (n-1)
    return [a + step * i for i in range(n)]


def chebyshev_nodes(a, b, n):
    return [0.5 * (a + b) + 0.5 * (b - a) * math.cos((2 * i + 1) * math.pi / (2 * n)) for i in range(n)]


def lagrange(X, Y, nodes=13, n=1000, chebyshev=False):
    if chebyshev:
        interpolation_nodes = chebyshev_nodes(0, len(X) - 1, nodes)
        interpolation_nodes = [int(i) for i in interpolation_nodes]
    else:
        interpolation_nodes = linspace(0, len(X) - 1, nodes)
        interpolation_nodes = [int(i) for i in interpolation_nodes]

    xs = linspace(X[0], X[-1], n)
    ys = [lagrange_function(X, Y, x, interpolation_nodes) for x in xs]

    return xs, ys, interpolation_nodes


def lagrange_function(X, Y, x, interpolation_nodes):
    value = 0
    for i in interpolation_nodes:
        y = 1
        for j in interpolation_nodes:
            if i == j:
                continue
            y *= (x - X[j]) / (X[i] - X[j])
        y *= Y[i]
        value += y

    return value


def cubic_spline(X, Y, nodes=5, n=1000):
    interpolation_nodes = linspace(0, len(X) - 1, nodes)
    interpolation_nodes = [int(i) for i in interpolation_nodes]

    k = len(interpolation_nodes)-1 #liczba przedzialow

    A = np.zeros((4*k, 4*k))
    B = np.zeros(4*k)

    #zrodlo, z ktorego korzystalem przy implementacji algorytmu
    #konstruujacego macierz A i wektor B
    #https://blog.timodenk.com/cubic-spline-interpolation/index.html

    #ustawianie wartosci wielomianow w wezlach interpolacji
    for i in range(k):
        x = X[interpolation_nodes[i]]
        xi = X[interpolation_nodes[i+1]]
        A[2*i][4*i:(4*i)+4] = [x**3, x**2, x, 1]
        B[2*i] = Y[interpolation_nodes[i]]

        A[2*i+1][4*i:(4*i)+4] = [xi**3, xi**2, xi, 1]
        B[2*i+1] = Y[interpolation_nodes[i+1]]

    #ustawianie wartosci pierwszych pochodnych w wewnetrzntch wezlach interpolacji
    for i in range(k-1):
        x = X[interpolation_nodes[i+1]]
        A[2*k+i][4*i:(4*i)+8] = [3*x**2, 2*x, 1, 0, -3*x**2, -2*x, -1, 0]

    #ustawianie wartosci drugich pochodnych w wewnetrznych wezlach interpolacji
    for i in range(k-1):
        x = X[interpolation_nodes[i+1]]
        A[3*k+i-1][4*i:(4*i)+8] = [6*x, 2, 0, 0, -6*x, -2, 0, 0]

    #ustawienie warunkow brzegowych (Natural Spline)
    A[4*k-2][0:2] = [6*X[0], 2]
    A[4*k-1][-4:] = [6*X[-1], 2, 0, 0]

    #rozwiazanie ukladu rownan - wspolczynniki a, b, c, d
    coeffs = np.linalg.solve(A, B)

    xs = linspace(X[0], X[-1], n)
    ys = [solve_polynomial(X, coeffs, xs[i], interpolation_nodes) for i in range(len(xs))]

    return xs, ys, interpolation_nodes


def solve_polynomial(X, coeffs, x_val, interpolation_nodes):
    for i in range(len(interpolation_nodes) - 1):
        if X[interpolation_nodes[i]] <= x_val <= X[interpolation_nodes[i + 1]]:
            a = coeffs[4*i]
            b = coeffs[4*i+1]
            c = coeffs[4*i+2]
            d = coeffs[4*i+3]
            return d + c*x_val + b*x_val**2 + a*x_val**3
    return 0
