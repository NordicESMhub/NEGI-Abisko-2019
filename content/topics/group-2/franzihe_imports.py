# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
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
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import seaborn as sns
import pandas as pd
import pyaerocom as pya
import franzihe_functions as fct
from glob import glob

# %%
pya.change_verbosity('critical', log=pya.const.print_log) # don't output warnings
pya.__version__

# %%
