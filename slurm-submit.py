#!/usr/bin/env python3

import logging
import os
import sys

from snakemake.utils import read_job_properties

logging.basicConfig(level=logging.INFO, filename="test.log")

jobscript = sys.argv[1]
job_properties = read_job_properties(jobscript)

resources = job_properties["resources"]
mem_mb = resources["mem_mb"]
cpus = resources["cpus"]
nodes = resources["nodes"]
runtime = resources["runtime"]
partition = resources["partition"]

# Create output log filename
# If wildcards are present, append them to the filename
rulename = job_properties["rule"]
wildcards = job_properties["wildcards"]
if wildcards:
    wildcard_str = "." + ".".join([f"{k}_{v}" for k, v in wildcards.items()])
else:
    wildcard_str = ""
slurm_log = f"slurm_out/{rulename}{wildcard_str}.log"

# Create slurm_out/ if it does not exist
wd = os.getcwd()
slurm_out_dir = f"{wd}/slurm_out"
if not os.path.exists(slurm_out_dir):
    os.mkdir(slurm_out_dir)

sbatch = (
    f"sbatch --nodes={nodes} --time={runtime} --cpus-per-task={cpus} "
    f"--mem={mem_mb} --partition={partition} --output={slurm_log} "
    f"{jobscript}"
)
os.system(sbatch)
