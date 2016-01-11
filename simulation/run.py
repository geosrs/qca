#!/usr/bin/python3

from cmath  import sqrt, sin, cos, pi
from collections import OrderedDict
from os.path import isfile
import numpy as np
from mpi4py import MPI
import matplotlib.pyplot as plt
import simulation.plotting as plotting
import simulation.time_evolve as time_evolve
import simulation.measures as measures
import simulation.fio as io
import time
import simulation.states as ss

# Execute simulations
# ===================

# lists of parameters to simulate
# -------------------------------
output_dir = 'tmp'

mode_list = ['alt']

L_list = [18]

T_list = [60]

S_list = [6]

V_list = ['H']

IC_list = ['c1l0']

BC_list = ['1']



#IC_list = [[ ('W', sin(th)), ('c1l0', cos(th))]
#        for th in np.linspace(0, pi/2.0, 10)]


params_list = [
           {
            'output_dir' : output_dir,
            'mode' : mode,
            'L' : L,
            'T' : T,
            'S' : S,
            'V' : V,
            'IC': IC,
            'BC': BC
             }

        for mode in mode_list  \
        for L    in L_list     \
        for T    in T_list     \
        for S    in S_list     \
        for V    in V_list     \
        for IC   in IC_list    \
        for BC   in BC_list    ]



# run independent simulations in parallel
# ---------------------------------------
if __name__ == '__main__':
    # initialize communication
    comm = MPI.COMM_WORLD
    # get the rank of the processor
    rank = comm.Get_rank()
    # get the number of processsors
    nprocs = comm.Get_size()
    # use rank 0 to give each simulation a file name
    if rank == 0:
        for params in params_list:
            if 'fname' in params:
                fname = params['fname']
            else:
                if 'IC' in params and params['IC'][0] == 'r':
                        fname = io.make_file_name(params, iterate = True)
                    # don't iterate file names with a unique IC name
                else:
                    fname = io.make_file_name(params, iterate = False)
                    # set the file name for each simulation
                params['fname'] = fname

    # boradcast updated params list to each core
    params_list = comm.bcast(params_list, root=0)
    for i, params in enumerate(params_list):

        # each core selects params to simulate without the need for a master
        if i % nprocs == rank:

            state_res = time_evolve.run_sim(params,
                    sim_tasks=['one_site', 'two_site', 'IPR'],
                    force_rewrite=True)
            res = measures.measure(params, state_res, force_rewrite=True)
            plotting.plot(params, res)
            plt.clf
    plt.close('all')
