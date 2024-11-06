#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1         # Cores per node
#SBATCH --partition=gpu3          # Partition name (skylake)
#SBATCH --gres=gpu:1
#SBATCH --job-name="lammps_md"
#SBATCH --time=00-00:30              # Runtime limit: Day-HH:MM
#SBATCH -o STDOUT.%N.%j.out          # STDOUT, %N : nodename, %j : JobID
#SBATCH -e STDERR.%N.%j.err          # STDERR, %N : nodename, %j : JobID
#SBATCH --reservation=hd


lmp_sevenn -in lammps.in > lammps.out
