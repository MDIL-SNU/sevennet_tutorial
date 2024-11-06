import matplotlib.pyplot as plt
import numpy as np
import sys

from scipy.stats import gaussian_kde
from scipy.stats import linregress
from sklearn.linear_model import LinearRegression

unit = {"energy": "eV/atom", "force": r"eV/$\rm{\AA}$", "stress": "kbar"}


def density_colored_scatter_plot(dft_energy, nnp_energy, dft_force, nnp_force, dft_stress, nnp_stress):
    modes = ['energy', 'force', 'stress']
    plt.figure(figsize=(18/2.54, 6/2.54))
    for num, (x, y) in enumerate(zip([dft_energy, dft_force, dft_stress], [nnp_energy, nnp_force, nnp_stress])):
        mode = modes[num]
        idx = np.random.choice(len(x), 1000) if len(x) > 1000 else list(range(len(x)))
        xsam = [x[i] for i in idx]
        ysam = [y[i] for i in idx]
        xy = np.vstack([x, y])
        xysam = np.vstack([xsam, ysam])
        zsam = gaussian_kde(xysam)

        z = zsam.pdf(xy)
        idx = z.argsort()

        x = [x[i] for i in idx]
        y = [y[i] for i in idx]
        z = [z[i] for i in idx]
        
        ax = plt.subplot(int(f'13{num+1}'))
        plt.scatter(x, y, c=z, s=4, cmap='plasma')

        mini = min(min(x), min(y))
        maxi = max(max(x), max(y))
        ran = (maxi-mini) / 20
        plt.plot([mini-ran, maxi+ran], [mini-ran, maxi+ran], color='grey', linestyle='dashed')
        plt.xlim(mini-ran, maxi+ran)
        plt.ylim(mini-ran, maxi+ran)

        plt.xlabel(f'DFT {mode} ({unit[mode]})')
        plt.ylabel(f'MLP {mode} ({unit[mode]})')
        ax.set_aspect('equal')

    plt.tight_layout()
    plt.show()


def read_per_atom(dirs):
    f = open(f"{dirs}/per_atom.csv")
    data = f.readlines()
    f.close()

    dft_force = []
    nnp_force = []

    for datum in data[1:]:
        dft_force.extend(list(map(float, datum.split(",")[7:10])))
        nnp_force.extend(list(map(float, datum.split(",")[10:13])))

    return dft_force, nnp_force


def read_per_graph(dirs):
    f = open(f"{dirs}/per_graph.csv")
    data = f.readlines()
    f.close()
    
    num_atoms = []
    dft_energy = []
    nnp_energy = []
    dft_stress = []
    nnp_stress = []

    for datum in data[1:]:
        num_atoms.append(int(datum.split(",")[0]))
        dft_energy.extend(list(map(float, datum.split(",")[2:3])))
        nnp_energy.extend(list(map(float, datum.split(",")[3:4])))
        dft_stress.extend(list(map(float, datum.split(",")[4:10])))
        nnp_stress.extend(list(map(float, datum.split(",")[10:16])))

    return num_atoms, dft_energy, nnp_energy, dft_stress, nnp_stress


def main():
    dirs = sys.argv[1]
    dft_force, nnp_force = read_per_atom(dirs)

    num_atoms, dft_energy, nnp_energy, dft_stress, nnp_stress = read_per_graph(dirs)

    dft_energy = [e/n for e, n in zip(dft_energy, num_atoms)]
    nnp_energy = [e/n for e, n in zip(nnp_energy, num_atoms)]

    density_colored_scatter_plot(dft_energy, nnp_energy, dft_force, nnp_force, dft_stress, nnp_stress)

main()
