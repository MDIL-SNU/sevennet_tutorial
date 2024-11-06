from sevenn.sevennet_calculator import SevenNetCalculator

from ase.io import read, write
from ase.constraints import UnitCellFilter
from ase.optimize import LBFGS
from ase.calculators.singlepoint import SinglePointCalculator

from copy import deepcopy
import sys
import numpy as np


def atom_oneshot(atoms, calc):
    energy = atoms.get_potential_energy()
    forces = atoms.get_forces()
    stress = atoms.get_stress()

    calc_results = {"energy": energy, "forces": forces, "stress": stress}
    calculator = SinglePointCalculator(atoms, **calc_results)
    atoms = calculator.get_atoms()

    return atoms


def atom_cell_relax(atoms, calc, logfile="-"):
    atoms.calc = calc
    cf = UnitCellFilter(atoms, hydrostatic_strain=True)
    opt = LBFGS(cf, logfile=logfile)
    opt.run(fmax=0.02, steps=1000)

    return atoms


def make_eos_structures(relaxed):
    relaxed_cell = relaxed.get_cell()
    relaxed_lat = relaxed_cell.lengths()[0]
    
    eos_structures = []
    for strain in np.linspace(-0.05, 0.05, 11):
        strained_lat = relaxed_lat * (1+strain)
        relaxed.set_cell([strained_lat]*3, scale_atoms=True)
        eos_structures.append(deepcopy(relaxed))

    return eos_structures


def main():
    log = open('log', 'w', buffering=1)
    atoms = read('/data2/HD_kits/sevennet/data/evaluation/eos.extxyz', ':')[5]
    model = sys.argv[1]

    calc = SevenNetCalculator(model=model)
    #calc = SevenNetCalculator(model='../../train/from_scratch/checkpoint_best.pth')
    #calc = SevenNetCalculator(model='7net-0_11July2024')

    relaxed = atom_cell_relax(atoms, calc, log)
    
    eos_structures = make_eos_structures(relaxed)
    eos_oneshot = []
    for structure in eos_structures:
        eos_oneshot.append(atom_oneshot(structure, calc))

    write('eos.extxyz', eos_oneshot)


main()

