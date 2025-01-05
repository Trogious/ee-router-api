import time


def timed(func):
    def wrapper(*arg, **kw):
        t1 = time.time_ns()
        res = func(*arg, **kw)
        t2 = time.time_ns()
        return int((t2 - t1) * 1e-6), res
    return wrapper
