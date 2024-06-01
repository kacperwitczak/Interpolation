from data import get_data
from utils import plot_data
from interpolation import lagrange, cubic_spline


def solve_profile(name):
    X, Y = get_data(name)

    indices_number = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    for nodes in indices_number:
        xs, ys, interpolation_nodes = lagrange(X, Y, nodes)
        plot_data(X, Y, xs, ys, interpolation_nodes, name + " Lagrange " + str(nodes) + " nodes")

        xs, ys, interpolation_nodes = lagrange(X, Y, nodes, chebyshev=True)
        plot_data(X, Y, xs, ys, interpolation_nodes, name + " Lagrange Chebyshev " + str(nodes) + " nodes")

        xs, ys, interpolation_nodes = cubic_spline(X, Y, nodes)
        plot_data(X, Y, xs, ys, interpolation_nodes, name + " Cubic Spline " + str(nodes) + " nodes")

def main():
    solve_profile("MountEverest")
    solve_profile("WielkiKanionKolorado")
    solve_profile("genoa_rapallo")


if __name__ == '__main__':
    main()