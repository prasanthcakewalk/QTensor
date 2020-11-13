# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/Speed_comparison.ipynb (unless otherwise specified).

__all__ = ['ex', 'graph', 'qiskit_time', 'quimb_time', 'qtensor_time']

# Cell
import numpy as np
import qtensor as qt
from qtensor.tests.qiskit_qaoa_energy import simulate_qiskit_amps
from qtensor.tests.qaoa_quimb import simulate_one_parallel as simulate_quimb_energy
import matplotlib.pyplot as plt
import time

from cartesian_explorer import Explorer

%load_ext autoreload
%autoreload 2

# Cell
ex = Explorer()

# Cell
@ex.provider
def graph(N, d=3, graph_type='random', seed=10):
    return qt.toolbox.random_graph(nodes=N, type=graph_type, degree=d, seed=seed)

# Cell
@ex.provider
def qiskit_time(graph, p):
    gamma, beta = [.1]*p, [.3]*p
    start = time.time()
    try:
        _ = simulate_qiskit_amps(graph, gamma, beta)
    except:
        return None
    end = time.time()
    return end - start

# Cell
@ex.provider
def quimb_time(graph, p,
               n_processes=2,
               qmb_optimizer_time=0.3,
               qmb_ordering_algo='uniform'
              ):
    start = time.time()
    try:
        _ = simulate_quimb_energy(graph, p,
                                  n_processes=n_processes,
                                  optimizer_time=qmb_optimizer_time,
                                  ordering_algo=qmb_ordering_algo
                                 )
    except:
        return None
    end = time.time()
    return end - start

# Cell
@ex.provider
def qtensor_time(graph, p,
               n_processes=2,
               qtn_ordering_algo='greedy'
              ):
    gamma, beta = [.1]*p, [.3]*p
    opt = qt.toolbox.get_ordering_algo(qtn_ordering_algo)
    sim = qt.QAOAQtreeSimulator(qt.DefaultQAOAComposer, optimizer=opt)
    start = time.time()
    try:
        _ = sim.energy_expectation_parallel(graph, gamma, beta, n_processes=n_processes)
    except:
        return None
    end = time.time()
    return end - start