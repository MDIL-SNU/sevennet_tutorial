import matplotlib.pyplot as plt
import numpy as np

def read_msd(filename):
    msd_list = []

    f = open(filename)
    data = f.readlines()
    f.close()

    for datum in data[1:]:
        d = datum.split()
        msd_list.append(float(d[-1]))

    return msd_list


def main():
    fine_tune_msd = read_msd('600.dat')
    dft_msd = read_msd('dft.dat')
    time_ft = np.linspace(0, 10/501*len(fine_tune_msd), len(fine_tune_msd))
    time_dft = np.linspace(0, 10, len(dft_msd))

    plt.figure(figsize=(10/2.54, 8/2.54))
    plt.plot(time_dft, dft_msd, marker='o', markersize=3, label='DFT')
    plt.plot(time_ft, fine_tune_msd, marker='^', markersize=3, label='Fine-tune')
    
    plt.legend()
    plt.xlabel('Time (ps)')
    plt.ylabel(r'MSD ($\rm{\AA}^2$)')
    plt.tight_layout()
    plt.show()


main()
