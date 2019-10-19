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

# %% [markdown]
# go to the dask array tab (shown below) and click on '<>'

# %% {"jupyter": {"source_hidden": true}}
from IPython.display import Image
Image(filename='dask.png',width=400)

# %% [markdown]
# something similar to the cell below should have being incerted

# %%
from dask.distributed import Client

client = Client("tcp://127.0.0.1:43878")
client

# %%
from negi_stuff.modules.imps import *
from pathlib import Path

# %%
df = cmip6.search_cmip6_hist(wildcard='mmrso4*',model='CESM*')
    

# %%
_ds = df.sort_values(['FORCING','REALIZATION'],ascending=[False,True])

# %%
_ds = df.sort_values(
    by       = [cmip6.FF,cmip6.RR,cmip6.FF],
    ascending= [False   ,True    ,True]
              )

# %%
_dg = _ds.groupby(cmip6.MODEL).first()

# %%
SIZE = 'SIZE'
df[SIZE] = df[cmip6.FILES].apply(lambda f: os.path.getsize(f))

# %%
_r = df.sort_values(SIZE, ascending=False).iloc[20]

# %%
_r['FILE_PATH']

# %%
large_file = '/home/28f6ea40-2d3059-2d4f6b-2d8429-2deb8e956423db/shared-cmip6-for-ns1000k/historical/CESM2/r11i1p1f1/mmrso4_AERmon_CESM2_historical_r11i1p1f1_gn_185001-189912.nc'

# %% [markdown]
# lets explore the dataset. 
# however this is not opening the dataset as a 
# [dask array] (https://examples.dask.org/xarray.html)

# %%
ds = xr.open_dataset(large_file)

# %%
#lets check the dimensions
ds.dims

# %%
#this will load the dataset as a dask array and therefore it will not kill the kernel
#some understanding of which operations you will perform on the dataset are needed
#in this case we are slicing the dataset along time
ds = xr.open_dataset(large_file,chunks={'time':1})

# %%
# this will run fast. but the mean has not being calculated just jet
ds['mmrso4'].mean()

# %%
# in order to get the actual value you need to load

# %%
ds['mmrso4'][{'time':slice(0,None)}].mean().load()

# %%
