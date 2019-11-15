# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
import numpy as np
import xarray as xr
#import negi_stuff.modules.zarray as za
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import importlib as il
import os
import glob
from datetime import datetime
import sys
import cartopy as crt
import random
from matplotlib.colors import LogNorm
import pyaerocom as pya


def load_and_reload():
    '''
    the code below automatically reload modules that
    have being changed when you run any cell.
    If you want to call in directly from a notebook you
    can use:
    Example
    ---
    >>> %load_ext autoreload
    >>> %autoreload 2
    '''
    from IPython import get_ipython

    try:
        _ipython = get_ipython()
        _ipython.magic('load_ext autoreload')
        _ipython.magic('autoreload 2')
    except:
        # in case we are running a script
        pass


load_and_reload()

