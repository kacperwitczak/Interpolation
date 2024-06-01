import matplotlib.pyplot as plt


def plot_data(X, Y, xs, ys, interpolation_nodes, name):
    plt.plot(X, Y, label='Oryginalna wartosc')
    plt.plot(xs, ys, label='Interpolacja')
    plt.scatter([X[i] for i in interpolation_nodes], [Y[i] for i in interpolation_nodes], label='Wezly interpolacji', color='red')
    plt.title(name)
    plt.xlabel("Dystans (m)")
    plt.ylabel("Wysokosc (m)")
    plt.legend()
    plt.show()