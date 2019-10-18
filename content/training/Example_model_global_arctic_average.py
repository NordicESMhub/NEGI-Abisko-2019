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
# # Example: Masked and weighted average:

# %% [markdown]
# This example focuses on area weights (weighting by the area of the grid cell), but is generalizable.  

# %%
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
# or
# from imports import (plt, np, xr)
path = '~/shared-cmip6-for-ns1000k/historical/NorESM2-LM/r1i1p1f1/tas_Amon_NorESM2-LM_historical_r1i1p1f1_gn_200001-200912.nc'
tas_ds = xr.open_dataset(path)

# %% [markdown]
# ## Get the area weigts:
# For the CMIP data, each model has a file for the area of each grid cell. The variable name of this is 'areacella'. We load the NorESM one. 

# %%
path_area_weight ='~/shared-cmip6-for-ns1000k/historical/NorESM2-LM/r1i1p1f1/areacella_fx_NorESM2-LM_historical_r1i1p1f1_gn.nc'
areacella= xr.open_dataset(path_area_weight)


# %% [markdown]
# ## A useful functions to do a weighted and masked average
#

# %%
def masked_average(xa, dim=None, weights=None, mask=None):
    """
    This function will average 
    :param xa: dataArray
    :param dim: dimension or list of dimensions. e.g. 'lat' or ['lat','lon','time']
    :param weights: weights (as xarray)
    :param mask: mask (as xarray), True where values to be masked.
    :return: masked average xarray
    """
    xa_ = xa.copy()
    if mask is not None:
        dum, mask_alld = xr.broadcast(xa, mask) # broadcast to all dims
        xa_ = xa_.where(np.logical_not(mask))
        if weights is not None:
            dum, weights_alld = xr.broadcast(xa, weights) # broadcast to all dims
            weights_alld = weights_alld.where(np.logical_not(mask_alld))
            return (xa_*weights_alld).sum(dim=dim)/weights_alld.where(xa_.notnull()).sum(dim=dim)
        else:
            return xa_.mean(dim)
    elif weights is not None:
        dum, weights_alld = xr.broadcast(xa, weights) # broadcast to all dims
        return (xa_*weights_alld).sum(dim)/weights_alld.where(xa_.notnull()).sum(dim=dim)
    else:
        return xa.mean(dim)



# %% [markdown]
# ## Application 1: Weigted global average:
# Grid cells have different area, so when we do the global average, they have to be weigted by the area of each grid cell. 
# Here we do it for 2 m temperature:

# %%
aw_xr = areacella['areacella']
glob_mean = masked_average(tas_ds['tas'], dim=['lat','lon'], weights=aw_xr)
glob_mean.plot()

# %% [markdown]
# ## Application 1: Weigted arctic average:
# Let's try to also take only the data above 60$^\circ$N

# %%
aw_xr = areacella['areacella']
# mask values with lat < 60 deg north
mask = tas_ds['lat']<60.
glob_mean = masked_average(tas_ds['tas'], dim=['lat','lon'], weights=aw_xr, mask=mask)
glob_mean.plot()
