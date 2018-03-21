import re, time, os

interactions = {}

from IPython.testing.globalipapp import get_ipython
from IPython.utils.io import capture_output

def get_ip():
    ip = get_ipython()
    ip.run_cell('%load_ext autoreload')        
    ip.run_cell('%autoreload 2')    
    ip.run_cell('import numpy as np')
    ip.run_cell('import matplotlib.pylab as plt')
    return ip

def run_cell(cmd):
    with capture_output() as io:
        res = get_ip().run_cell(cmd)
    res_out = io.stdout
    return res_out

