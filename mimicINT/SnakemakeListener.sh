#!/bin/bash

# -------------------------------------------------------------------------
# VARIABLE BELOW MUST BE CHANGED TO BE ADAPTED TO THE FOLDER STRUCTURE
# AND THE SNAKEMAKE COMMAND TO EXECUTE
# -------------------------------------------------------------------------

# Folder containinh the analysis folders
ROOT_FOLDER=/home/mimicint/tagc-mimicweb/tagc-mimicint/jobs
TOOLS_FOLDER=${ROOT_FOLDER}/tools

# Name of the file indicating a snakmake workflow have to be launched
TRIGGER_FILE=start_snakemake

SNAKEMAKE_LOG_FILE="snakemake.log"

#CHANGE PERMISSIONS JOBS FOLDER

# -------------------------------------------------------------------------
# CODE BELOW DETECT THE TRIGGER FILES AND LAUNCH THE SNAKEMAKE COMMAND
# DO NOT CHANGE
# -------------------------------------------------------------------------

# Building the listener log file if it does not exists
listener_log_file=$ROOT_FOLDER/listerner.log
if [ ! -f "$listener_log_file" ]; then
    touch $listener_log_file
fi

#State the listener starts
echo "$(date) Starting listener" >> $listener_log_file

# Looking for trigger files
cd $ROOT_FOLDER
trigger_file_list=$(find $ROOT_FOLDER -type f -name "$TRIGGER_FILE")

# Loop over trigger files to launch snakemake workflows
for trigger_file in $trigger_file_list
do
	# Indicate in the listener log file the foudn trigger
	echo "|--$(date) : New trigger found:" $trigger_file >> $listener_log_file

	# Get the trigger file folder (i.e. the snakemake workflow folder)
	job_folder=$(dirname $trigger_file)
	echo "|--|--Folder is:" $job_folder >> $listener_log_file

	# Change dir to the trigger folder and tun snakemake command with nohup
	cd $job_folder

	echo "Job_folder=" $job_folder > log_version.txt
	echo "Current folder=" $(pwd) >> log_version.txt

        nohup docker exec docker-centos7-slurm-snakemake /bin/bash -c "cd $job_folder && snakemake --snakefile $job_folder/workflow/mimicint_interpro_snakefile \
                  --use-singularity \
                  --singularity-args='-B $(pwd):$(pwd) -B $(pwd)/../mimicINT_InterPro:$(pwd)/../mimicINT_InterPro -B ${TOOLS_FOLDER}/iupred:/iupred' \
                  --jobs 2 \
                  --reason \
            --cluster-config config/config_cluster.json \
                    --cluster 'sbatch \
                                -A {cluster.project} \
                                --job-name {cluster.job-name} \
                                --partition {cluster.partition} \
                                --time {cluster.time} \
                                --mem {cluster.mem} \
                                -c {threads} \
                                --mail-user {cluster.mail-user} \
                                --mail-type {cluster.mail-type} \
                                --error {cluster.error} \
                                --output {cluster.output}' \
                  2> error_$SNAKEMAKE_LOG_FILE 1>$SNAKEMAKE_LOG_FILE" &

	cd $ROOT_FOLDER
	echo "|--|--Snakemake command launched " >> $listener_log_file

	# Remove the trigger file to avoid new launch in that folder
	rm -f $trigger_file
	echo "|--|--Trigger file removed " >> $listener_log_file
done


