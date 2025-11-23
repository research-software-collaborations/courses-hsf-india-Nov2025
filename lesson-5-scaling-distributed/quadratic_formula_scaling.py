# writing to a separate file, because multiprocessing is buggy in notebooks (see: https://bugs.python.org/issue25053)
import numpy as np
import time

a = np.random.uniform(5, 10, 1_000_000)
b = np.random.uniform(10, 20, 1_000_000)
c = np.random.uniform(-0.1, 0.1, 1_000_000)

def quadratic_formula(task_id):
    time.sleep(task_id / 5.0)  # simulate some task_id-dependent workload
    return (-b + np.sqrt(b**2 - 4*a*c)), task_id  # return task_id for identification


# setup 10 tasks
task_ids = range(10)
