#!/bin/bash
#SBATCH --partition=dg-jup
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --nodelist=dg-gpunode02
#SBATCH --gres=gpu:6
#SBATCH --mem=128G
#SBATCH --time=4:00:00
#SBATCH --job-name=BigBody
# %x=job-name %j=jobid
#SBATCH --output=%x_%j.out
# 
# change to the directory where you submitted this script
cd ${SLURM_SUBMIT_DIR}
#
# your job execution follows:
echo "Starting sbatch script myscript.sh at:`date`"
# echo some slurm variables for fun
echo "  running host:    ${SLURMD_NODENAME}"
echo "  assigned nodes:  ${SLURM_JOB_NODELIST}"
echo "  jobid:           ${SLURM_JOBID}"
# show me my assigned GPU number(s):
echo "  GPU(s):          ${CUDA_VISIBLE_DEVICES}"

source activate deeplearning
python run.py
