#!/bin/bash

# -------------------------------------------------------------------------
# VARIABLE BELOW MUST BE CHANGED TO BE ADAPTED TO THE FOLDER STRUCTURE
# AND THE SLURM COMMAND TO EXECUTE
# -------------------------------------------------------------------------

# Folder containing the analysis folders
ROOT_FOLDER=/home/mimicint/tagc-mimicweb/tagc-mimicint/jobs

# -------------------------------------------------------------------------
# CODE BELOW DETECT THE TRIGGER FILES AND LAUNCH THE SNAKEMAKE COMMAND
# DO NOT CHANGE
# -------------------------------------------------------------------------

# Building the listener log file if it does not exists
listener_log_file=$ROOT_FOLDER/slurm_listerner.log
if [ ! -f "$listener_log_file" ]; then
    touch $listener_log_file
fi

#State the listener starts
echo "$(date) Starting SLURM listener" >> $listener_log_file

# Ask for the slumr queue content
#docker exec docker-centos7-slurm-snakemake squeue -"o%j %i %T " -h > $ROOT_FOLDER/slurm_squeue.txt
docker exec docker-centos7-slurm-snakemake squeue -"o%j %T " -h > $ROOT_FOLDER/slurm_squeue.txt

