import xarray as xr
import numpy as np
import glob as glob
import matplotlib.pyplot as plt

def compute_model_profile_10km(path_to_model_data_folder):
    """
    This function computes the temporal and spatial averaged profiles of 
    modelled aerosol extinction coefficient found in the input path. 
    
    Returns: area weighted averaged aerosol extinction profile for the Arctic region
    """
    path_extinction=glob.glob(path_to_model_data_folder+'/renamed/*ec550aer*_2010_monthly.nc')
    path_dh=glob.glob(path_to_model_data_folder+'/renamed/*dh*_2010_monthly.nc')
    path_orog=glob.glob(path_to_model_data_folder+'/renamed/*orog*.nc')
    path_areacella=glob.glob(path_to_model_data_folder+'/renamed/*areacella*.nc')
    areacella=xr.open_dataset(path_areacella[0])
    aw_xr = areacella['areacella']
    extinction = xr.open_dataset(path_extinction[0])
    extinction=extinction['ec550aer'].sel(lat=slice(70,90))
    layer_thickness= xr.open_dataset(path_dh[0])
    layer_thickness=layer_thickness['dh'].sel(lat=slice(70,90))
    orog=xr.open_dataset(path_orog[0])
    orog=orog['orog'].sel(lat=slice(70,90))
    profile_model_extinction = masked_average(extinction,dim = ['lat','lon','time'],weights=aw_xr)*1000    
    profile_model_height = compute_model_levels(layer_thickness, orog,aw_xr)
    mask = profile_model_height < 10
    profile_model_extinction_10km = profile_model_extinction[mask.values]
    profile_model_height_10km=profile_model_height[mask.values]
    return (profile_model_extinction_10km,profile_model_height_10km)

def compute_seasonal_model_profile_10km(path_to_model_data_folder,low_month):
    """
    This function computes the seasonal and spatial averaged profiles of 
    modelled aerosol extinction coefficient found in the input path. 
    
    It considers four standard seasons (D-J-F, M-A-M, J-J-A, S-O-N).
    
    To specify the season give the input of the index of lowest month. 
    For e.g., the season index for D-J-F is the index of the lowest month December i.e. -1.
    The indices for all the seasons is (-1,3,6,9). 
    
    
    Returns: seasonal area weighted averaged aerosol extinction profile for the Arctic region
    """
    path_extinction=glob.glob(path_to_model_data_folder+'/renamed/*ec550aer*_2010_monthly.nc')
    path_dh=glob.glob(path_to_model_data_folder+'/renamed/*dh*_2010_monthly.nc')
    path_orog=glob.glob(path_to_model_data_folder+'/renamed/*orog*.nc')
    path_areacella=glob.glob(path_to_model_data_folder+'/renamed/*areacella*.nc')
    areacella=xr.open_dataset(path_areacella[0])
    aw_xr = areacella['areacella']
    extinction = xr.open_dataset(path_extinction[0])
    extinction=extinction['ec550aer'][[low_month,low_month+1,low_month+2],:,:,:]
    extinction=extinction.sel(lat=slice(70,90))
    layer_thickness= xr.open_dataset(path_dh[0])
    layer_thickness=layer_thickness['dh'][[low_month,low_month+1,low_month+2],:,:,:]
    layer_thickness=layer_thickness.sel(lat=slice(70,90))
    orog=xr.open_dataset(path_orog[0])
    orog=orog['orog'].sel(lat=slice(70,90))
    profile_model_extinction = masked_average(extinction,dim = ['lat','lon','time'],weights=aw_xr)*1000    
    profile_model_height = compute_model_levels(layer_thickness, orog,aw_xr)
    mask = profile_model_height < 10
    profile_model_extinction_10km = profile_model_extinction[mask.values]
    profile_model_height_10km=profile_model_height[mask.values]
    return (profile_model_extinction_10km,profile_model_height_10km)

def compute_model_levels(model_layer_thickness, model_orog,aw_xr):
    """
    This is a helper function for compute_model_profile_10km() and compute_seasonal_model_profile_10km().
    
    This function computes the model levels in units of kilometers. 
    It uses the model layer thickness and the height of the surface elevation (orography)
    
    Return: model vertical levels (in km)    
    """
    cum_model_thickness= model_layer_thickness.cumsum(dim='lev', skipna='True')
    net_model_level = model_orog + cum_model_thickness
    profile_model_height = masked_average(net_model_level,dim=['lat','lon','time'],weights=aw_xr)/1000    #to convert the units from m to km
    return (profile_model_height)

def set_axis_profiles_model_caliop(axs):
    """
    This function computes the temporal and spatial averaged profiles of 
    modelled aerosol extinction coefficient found in the input path. 
    
    Returns: area weighted averaged aerosol extinction profile for the Arctic region
    """
    axs[0].set_xlabel('Extinction Coefficient (km -1)',fontsize=12, fontweight='bold')
    axs[0].set_ylabel('Height (km)',fontsize=12, fontweight='bold')
    axs[1].set_xlabel('Normalised Extinction Coefficient ',fontsize=12, fontweight='bold')
    axs[1].set_ylabel('Height (km)',fontsize=12, fontweight='bold')
    axs[1].legend()
    axs[0].legend()
    return axs

def normalised_profile(data_array):
    """
    function to normalise an array
    """
    norm=(data_array- np.min(data_array))/(np.max(data_array)-np.min(data_array))
    return norm

def mean_extinction_height(profile_array,height_array):
    """
    This function computes the mean extinction height. 
    profile_array: this is an xarray of the extinction profile
    height_array: xarray: corresponding profile altitude (in km) 
    Returns: mean extinction height for the Arctic region
    """
    Zo=((profile_array*height_array).sum()/profile_array.sum())
    return Zo

def compute_seasonal_caliop_profile_10km(extinction_caliop_10km,low_month):
    """
    This function computes the seasonal aerosol extinction coefficient 
    from the caliop satellite data.
    
    extinction_caliop_10km: caliop extinction profiles sliced up to 10 km altitude
    It considers four standard seasons (D-J-F, M-A-M, J-J-A, S-O-N).
    
    low_month: To specify the season give the input of the index of lowest month. 
    For e.g., the season index for D-J-F is the index of the lowest month December i.e. -1.
    The indices for all the seasons is (-1,3,6,9). 
    """
    s=extinction_caliop_10km[[low_month,low_month+1,low_month+2],:,:,:].mean(dim=('latitude','longitude','time'))
    return s

def get_done_titles(ax):
    """
    This function gives titles to all the subplots in the seasonal profiles of aerosol extinction coefficient
    """
    ax[0].set_xlabel('D - J - F',fontsize=12, fontweight='bold')
    ax[1].set_xlabel('M - A - M',fontsize=12, fontweight='bold')
    ax[2].set_xlabel('J - J - A',fontsize=12, fontweight='bold')
    ax[3].set_xlabel('S - O - N',fontsize=12, fontweight='bold')
    return(ax)


def masked_average(xa:xr.DataArray,
                   dim=None,
                   weights:xr.DataArray=None,
                   mask:xr.DataArray=None):
    """
    This function will average
    :param xa: dataArray
    :param dim: dimension or list of dimensions. e.g. 'lat' or ['lat','lon','time']
    :param weights: weights (as xarray)
    :param mask: mask (as xarray), True where values to be masked.
    :return: masked average xarray
    """
    #lest make a copy of the xa
    xa_copy:xr.DataArray = xa.copy()

    if mask is not None:
        xa_weighted_average = __weighted_average_with_mask(
            dim, mask, weights, xa, xa_copy
        )
    elif weights is not None:
        xa_weighted_average = __weighted_average(
            dim, weights, xa, xa_copy
        )
    else:
        xa_weighted_average =  xa.mean(dim)

    return xa_weighted_average



    # %% [markdown]


def __weighted_average(dim, weights, xa, xa_copy):
    '''helper function for masked_average'''
    _, weights_all_dims = xr.broadcast(xa, weights)  # broadcast to all dims
    x_times_w = xa_copy * weights_all_dims
    xw_sum = x_times_w.sum(dim)
    x_tot = weights_all_dims.where(xa_copy.notnull()).sum(dim=dim)
    xa_weighted_average = xw_sum / x_tot
    return xa_weighted_average


def __weighted_average_with_mask(dim, mask, weights, xa, xa_copy):
    '''helper function for masked_average'''
    _, mask_all_dims = xr.broadcast(xa, mask)  # broadcast to all dims
    xa_copy = xa_copy.where(np.logical_not(mask))
    if weights is not None:
        _, weights_all_dims = xr.broadcast(xa, weights)  # broadcast to all dims
        weights_all_dims = weights_all_dims.where(~mask_all_dims)
        x_times_w = xa_copy * weights_all_dims
        xw_sum = x_times_w.sum(dim=dim)
        x_tot = weights_all_dims.where(xa_copy.notnull()).sum(dim=dim)
        xa_weighted_average = xw_sum / x_tot
    else:
        xa_weighted_average = xa_copy.mean(dim)
    return xa_weighted_average


def set_axes_extinction_height(ax,seasonid,seasonname):
    """
    This function sets the labels and ticks for the figure showing the seasonal variation of extinction height 
    """
    plt.xlabel('Seasons',fontsize=14) 
    plt.ylabel('Mean extinction height (km)',fontsize=14) 
    plt.xticks(seasonid,seasonname) 
    plt.title('Seasonal variation of mean extinction height over the Arctic',fontsize=18)
    legend=ax.legend(loc='upper center', bbox_to_anchor=(1.25, 0.8), shadow=True, ncol=1)
    legend.get_frame().set_facecolor('w')
    return ax