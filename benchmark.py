#!/bin/python
import subprocess
import sys

from time import sleep


n_jobs = list(range(1, 9))
n_samples = [1000, 10**6, 10**8]
SLEEP_TIME = 4

flags = {
        '--local':   ['mpiexec', '-np', 'jobs', './a.out', 'samples'],
        '--cluster':     ['sbatch', '-n', 'jobs', './run_sbatch_config.sh', 'samples'],
    }

run_cmd = flags['--cluster']

if len(sys.argv) > 1:
    try:
        run_cmd = flags[sys.argv[1]]
    except KeyError:
        pass

stats = dict.fromkeys(n_samples)

for samples in n_samples:
    stats[samples] = dict.fromkeys(n_jobs)
    for job_count in n_jobs:
        run_cmd[2] = str(job_count)
        run_cmd[4] = str(samples)

        subprocess.run(run_cmd)
        sleep(SLEEP_TIME)
        
        with open('output.txt', 'r') as f:
            data = f.readlines[-2:]
            stats[samples][job_count] = (float(data[0]), float(data[1]))

for samples in n_samples:
    print('SINGLE\tPARALLEL')
    for job_count in n_jobs:
        print(str(stats[samples][job_count][0]) + '\t' + str(stats[samples][job_count][1]))

