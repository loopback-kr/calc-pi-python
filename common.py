import os, typing, argparse, multiprocessing.pool as mpp

"""
Implementation of Multi-processing
"""
def istarmap(self, func, iterable, chunksize=1):
    """
    starmap-version of imap
    """
    self._check_running()
    if chunksize < 1:
        raise ValueError(
            "Chunksize must be 1+, not {0:n}".format(
                chunksize))

    task_batches = mpp.Pool._get_tasks(func, iterable, chunksize)
    result = mpp.IMapIterator(self)
    self._taskqueue.put((
            self._guarded_task_generation(result._job, mpp.starmapstar, task_batches),
            result._set_length
        ))
    return (item for chunk in result for item in chunk)
mpp.Pool.istarmap = istarmap

def run_multiproc(func, *args, total:int=None, desc='', num_processes=os.cpu_count()):
    args = list(args)
    if total is None:
        total = len(args[0])
    num_proc = total
    rets = []
    for idx, arg in enumerate(args[1:], start=1):
        if not isinstance(arg, typing.Iterable) or isinstance(arg, str) or len(arg) != num_proc:
            args[idx] = [arg] * num_proc
    
    with mpp.Pool(min(os.cpu_count(), num_processes)) as pool:
        for ret in pool.istarmap(func, zip(*args)):
            rets.append(ret)
    return rets
