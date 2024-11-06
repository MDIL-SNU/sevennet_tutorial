#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1         # Cores per node
#SBATCH --partition=gpu3          # Partition name (skylake)
#SBATCH --gres=gpu:1
#SBATCH --job-name="fine_tune"
#SBATCH --time=00-00:30              # Runtime limit: Day-HH:MM
#SBATCH -o STDOUT.%N.%j.out          # STDOUT, %N : nodename, %j : JobID
#SBATCH -e STDERR.%N.%j.err          # STDERR, %N : nodename, %j : JobID
#SBATCH --reservation=hd


sevenn fine_tune.yaml
