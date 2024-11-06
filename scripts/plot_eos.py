import matplotlib.pyplot as plt
import numpy as np
from ase.io import read

def get_eos_and_volume(eos_list):
    en_list = []
    vol_list = []
    for atoms in eos_list:
        en_list.append(atoms.get_potential_energy())
        vol_list.append(atoms.get_volume())
        
    rel_en_list = np.array(en_list) - min(en_list)

    return rel_en_list, vol_list


def main():
    dft_eos, dft_vol = get_eos_and_volume(read('/data2/HD_kits/sevennet/data/evaluation/eos.extxyz', ':'))
    ft_eos, ft_vol = get_eos_and_volume(read('fine_tune.extxyz', ':'))
    fs_eos, fs_vol = get_eos_and_volume(read('from_scratch.extxyz', ':'))
    svn_0_eos, svn_0_vol = get_eos_and_volume(read('7net_0.extxyz', ':'))

    plt.figure(figsize=(10/2.54, 8/2.54))
    plt.plot(dft_vol, dft_eos, label='DFT')
    plt.plot(ft_vol, ft_eos, label='Fine-tuning')
    plt.plot(fs_vol, fs_eos, label='From scratch')
    plt.plot(svn_0_vol, svn_0_eos, label='7net-0')

    plt.xlabel(r"Volume ($\rm{\AA}^3$)")
    plt.ylabel("Relative energy (eV)")

    plt.legend()
    plt.tight_layout()
    plt.show()

main()
