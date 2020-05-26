"""
wrappers
"""

import time

def timeTaken(func):
        def wrapper(*args, **kwargs):
                start = time.time()
                func(*args, **kwargs)
                end = time.time()
                print(str(func) + " > Time taken : ", end-start)
                #print("args are : ", args)
                #print("keyword args are : ", kwargs)
        return wrapper