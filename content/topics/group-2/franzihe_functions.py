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
from franzihe_imports import (xr, np, pd, pya, plt, sns)
from glob import glob


# %%
def plot_style():
    plt.style.use('ggplot')
    sns.set_context('poster')
    sns.set(font = 'Serif', font_scale = 2, )
    sns.set_style('darkgrid',
                  {'font.family':'serif', #'font.serif':'Helvetica'
                   'grid.linestyle': '--'           },
                   )
plot_style()


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
            return (xa_*weights_alld).sum(dim=dim)/weights_alld.sum(dim=dim)
        else:
            return xa_.mean(dim)
    elif weights is not None:
        dum, weights_alld = xr.broadcast(xa, weights) # broadcast to all dims
        return (xa_*weights_alld).sum(dim)/weights_alld.where(xa_.notnull()).sum(dim=dim)
    else:
        return xa.mean(dim)



# %%
def read_all_cmip6_od550aer(cmip6_model,hist_path,chunks, 
                            lower_lat, upper_lat,
                            lower_lon, upper_lon,
                            starty, endy):
    """Finds all cmip6 model outputs which contain o55aer and returns a dictonary which contains the models
    as well as the different realisations with cmip.
    The weighted average will also be calculated for given latitude and longitude.
    Median and standard deviation will be created for given latitude, longitude, starting and endying year.
    
    Parameters:
    -----------
    hist_path   : pre-defined directory
    cmip6_model : model names found in pre-defined directory
    chunks      : for dask import
    lower_lat   : lower latitude boundary for weighted averag
    upper_lat   : upper latitude boundary --- "" ---
    lower_lon   : lower longitude boundary --- "" ---
    upper_lon   : upper longitude bounary --- "" ---
    starty      : as string beginning of anaylsis
    endy        : as string end of analysis
    """
    cmip = {}
    for mp in range(len(cmip6_model)):
        mp_n = cmip6_model[mp]
        cmip[mp_n] = {}
        # loop over realisations (e.g the r1i1p1f2)
        for rea in glob(hist_path + cmip6_model[mp] + '/*'):
            _r = rea.split('/')[-1]
            fn_list = [fn for fn in glob(hist_path + cmip6_model[mp]+ '/%s/od550aer_AERmon_*.nc'%_r) if (int(fn[-9:-5])>1980)]
            fn_areac= [fn for fn in glob(hist_path + cmip6_model[mp]+ '/%s/areacella*.nc'%_r)]
            fn_list.sort()
            fn_areac.sort()
            
            if len(fn_list)>0:
                _ds= xr.open_mfdataset(fn_list, chunks=chunks,parallel=True, use_cftime = True)

                if len(fn_areac)>0 and fn_list[0][-20:-17] == fn_areac[0][-6:-3]:
                    _dsa = xr.open_dataset(fn_areac[0], use_cftime = True)
                    _ds['areacella'] = _dsa['areacella']
                

                cmip[mp_n][_r] = _ds

                # Shift the longitude from 0-->360 to -180-->180 and sort by longitude and time
                cmip[mp_n][_r] = cmip[mp_n][_r].assign_coords(lon=(((cmip[mp_n][_r].lon + 180) % 360) - 180)).sortby('lon').sortby('time')
            
                
    return(cmip)


# %%
def read_merra2(path,oldc_name,newc_name):
    """Reads the csv files obtained from MERRA2
    
    Parameters:
    -----------
    path     : location and filename of MERRA2 data
    oldc_name: column name as it is in csv file
    newc_name: column name as it should be"""
    merra = pd.read_csv(path, 
                    header = 7, 
                    index_col = 'time', 
                    parse_dates=True, 
                    skipinitialspace=True)
    merra.rename(columns={oldc_name : newc_name}, inplace=True)
    
    return(merra)


# %%
def read_merra2_zonal(_dir):
    """Reads the zonal csv files obtained from MERRA2
    Parameters:
    -----------
    _dir : location/filename of MERRA2 data"""
    
    # find zonal csv files
    fn_list = glob(_dir)
    fn_list.sort()
    merra_zonal={}
    for i in range(len(fn_list)):
        _zonal = pd.read_csv(fn_list[i], header=6, #index_col = 'latitude (degrees north)',
                                                                              skipinitialspace=True)
        #_zonal.rename(columns={'M2IMNXGAS_5_12_4_AODANA': fn_list[i][49:53] +'_' + fn_list[i][58:62]}, inplace=True)
        _zonal.insert(loc=1, column = 'lat', value=np.arange(-90,90.5,0.5))
        _zonal = _zonal.set_index('lat')
    
        merra_zonal[fn_list[i][49:53]+fn_list[i][58:62]] = _zonal.to_xarray()
        
    return(merra_zonal)


# %%
def read_aerocom_return_xarray_median_std(pyaero_path, lower_lat, upper_lat, starty, endy):
    """Reads the AOD from the sunphotometer at chosen stations for chosen years 
    and returns an xarry including median and standard deviation
    
    Parameters:
    -----------
    pyaero_path : location of pyaerocom data
    lower_lat   : choose stations above this latitude
    upper_lat   : choose stations below this latitude
    starty      : start year for analysis
    endy        : end year for analysis"""
    pya.const.BASEDIR = pyaero_path
    
    aeronet_arctic = pya.io.ReadUngridded().read('AeronetSunV3Lev2.daily', 'od550aer').apply_filters(latitude=(lower_lat, upper_lat))
    
    ## transform aerocom data to xarray
    an_arctic = {}

    for station_name in aeronet_arctic.unique_station_names:
        an_arctic[station_name] = {}
        an_arctic[station_name]['od550aer'] = aeronet_arctic.to_station_data(station_name)['od550aer'].to_xarray()
        ## insert station coordinates
        an_arctic[station_name]['longitude'] = aeronet_arctic.to_station_data(station_name)['longitude']
        an_arctic[station_name]['latitude'] = aeronet_arctic.to_station_data(station_name)['latitude']
        
        ## calculate median and standard deviation of aerocom data
        an_arctic[station_name]['median_'+starty+endy] = {}
        an_arctic[station_name]['std_'+starty+endy]    = {}
        if len(an_arctic[station_name]['od550aer'].sel(index=slice(starty + '-01', endy + '-12'))) > 0:
            an_arctic[station_name]['median_'+starty+endy] = an_arctic[station_name]['od550aer'].sel(index=slice(starty + '-01', endy + '-12')).groupby('index.month').median(skipna=True)
            an_arctic[station_name]['std_'+starty+endy]    = an_arctic[station_name]['od550aer'].sel(index=slice(starty + '-01', endy + '-12')).groupby('index.month').std(skipna=True)
        
    return(an_arctic)


# %%
def read_merra2_return_xarray_median_std(aeronet, merra_file, starty, endy):
    """Reads the AOD from MERRA2 at chosen stations for chosen years 
    and returns an xarry including median and standard deviation
    
    Parameters:
    -----------
    aeronet    : pyaerocom xarray 
    merra_file : location and filename of MERRA2 data
    starty     : start year for analysis
    endy       : end year for analysis"""
    
    merra_st = pd.DataFrame()
    merra = {}
    for station_name in aeronet.keys():
        _long = aeronet[station_name]['longitude']
        _lat  = aeronet[station_name]['latitude']
        if _long < 0:
            _direction = 'W'
        if _long > 0:
            _direction = 'E'
        fn = glob(merra_file + '*%s%s_%sN.csv' %(str(int(abs(_long))),
                                                      _direction,str(int(_lat))))
        merra[station_name] = {}
        merra[station_name]['od550aer'] = xr.DataArray(read_merra2(fn[0], 'mean_M2IMNXGAS_5_12_4_AODANA', station_name)[station_name],dims=['index',])
        ## calculate median and standard deviation of MERRA2
        merra[station_name]['median_'+starty+endy] = merra[station_name]['od550aer'].sel(index=slice(starty + '-01', endy + '-12')).groupby('index.month').median(skipna=True)
        merra[station_name]['std_'+starty+endy] = merra[station_name]['od550aer'].sel(index=slice(starty + '-01', endy + '-12')).groupby('index.month').std(skipna=True)

    return(merra)


# %%
def calc_xarray_median_std_monthly(xarray, variable, starty, endy):
    """Calculate the median and standard deviation monthly of an AOD at the station for
    a given time range
    
    Parameters:
    -----------
    xarray       : xarray holding the AOD data
    station_name : name of the station
    starty       : start year for analysis
    endy         : end year for analysis"""
    xarray['median_'+starty+endy] = xarray[variable].sel(time=slice(starty + '-01', endy + '-12')).groupby('time.month').median(skipna=True)
    xarray['std_'+starty+endy]    = xarray[variable].sel(time=slice(starty + '-01', endy + '-12')).groupby('time.month').std(skipna=True)
    
    return(xarray)


# %%
def calc_xarray_median_std_yearly(xarray, variable, starty, endy):
    """Calculate the median and standard deviation yearly of an AOD at the station for
    a given time range
    
    Parameters:
    -----------
    xarray       : xarray holding the AOD data
    station_name : name of the station
    starty       : start year for analysis
    endy         : end year for analysis"""
    xarray['median_'+starty+endy] = xarray[variable].sel(time=slice(starty+'-01', endy+'-12')).median('time',skipna=True,keep_attrs=True)
    xarray['std_'+starty+endy]    = xarray[variable].sel(time=slice(starty+'-01', endy+'-12')).std('time',skipna=True,keep_attrs=True)
    
    return(xarray)


# %%
def calc_weighted_av_median_std(cmip,starty, endy,model,
                                mask=None, dim=None, 
                                lower_lat=None, upper_lat=None, 
                                lower_lon=None, upper_lon=None,
                                ):
    """Calculate the weighted average with function given on NEGI-2019 web page.
    Afterwards calculate the median and standard deviation of the area weighted cells.
    
    Parameters:
    -----------
    cmip       : CMIP models dictionary
    starty     : start year for analysis
    endy       : end year for analysis
    model      : model to be analysed
    mask       : mask (as xarray), True where values to be masked.
    dim        : dimension or list of dimensions. e.g. 'lat' or ['lat','lon','time']
    lower_lat   : lower latitude boundary for weighted averag
    upper_lat   : upper latitude boundary --- "" ---
    lower_lon   : lower longitude boundary --- "" ---
    upper_lon   : upper longitude bounary --- "" ---
    """
    
    try:
        aw_xr = cmip['areacella']
        area_weight = masked_average(cmip['od550aer'].sel(time = slice(starty + '-01', endy + '-12'),
                                                             lat  = slice(lower_lat, upper_lat),
                                                             lon  = slice(lower_lon, upper_lon)),
                                   dim=dim,
                                   weights=aw_xr,
                                   mask=mask)
        cmip['median_'+starty+endy] = area_weight.sel(time=slice(starty+'-01',endy+'12')).groupby('time.month').reduce(np.nanpercentile, dim='time', q=0.5)
        cmip['std_'+starty+endy] = area_weight.sel(time=slice(starty+'-01',endy+'12')).groupby('time.month').std(keep_attrs=True, skipna=True)

    except KeyError:
        print('no areacella data: %s - %s' %(starty,endy), model )
    return(cmip)


# %%
def calc_statistic(aeronet, merra, starty, endy):
    """Calculates the statistics for two variables. Returns list, 
    containing variables as described in pyaerocom.mathutils.calc_statistics.
    
    Parameters:
    -----------
    aeronet : reference values
    merra   : values which shall be compared
    starty  : string of statistic begin
    endy    : string of statistic end"""

    result_an = pd.DataFrame()
    result_me = pd.DataFrame()
    result_me_arct = pd.DataFrame()
    for station_name in aeronet.keys():
        # for aeronet and Merra2 stations
        if len(aeronet[station_name]['median_'+starty+endy]) <= 0 or len(aeronet[station_name]['std_'+starty+endy]) <=0:
            continue
        else:
            # concat the valid aeronet stations for statistics
            result_an = pd.concat([result_an, aeronet[station_name]['median_'+starty+endy].to_dataframe(station_name)],axis=1)
            # concat the valid merra2 stations for statistics
            result_me = pd.concat([result_me, merra[station_name]['median_'+starty+endy].to_dataframe(station_name)],axis=1)
         # for Merra2 arctic 
        result_me_arct = pd.concat([result_me_arct, merra['M_Arctic']['median_'+starty+endy].to_dataframe()],axis=1)
    # calculate scatter plot statistcis
    stat_stations = pya.mathutils.calc_statistics(result_me[result_an.index[0]-1: result_an.index[-1]].values.flatten(), result_an.values.flatten())
    stat_merra    = pya.mathutils.calc_statistics(result_me.values.flatten(), result_me_arct.values.flatten() )
    
    return(stat_stations, stat_merra)


# %%
def plt_scatter(x, y, xlim, ylim, xlabel, ylabel,
                statistics, subfig_label, ax, color):
    """Plots a logarithmic scatter plot an annoates with statistic
    
    Parameters:
    -----------
    x            : reference value
    y            : values which shall be compared
    ylim         : limit of the yaxis
    xlabel       : name of the xaxis
    ylabel       : name of the yaxis
    statistics   : statistical properties
    subfig_label : title of the subplot
    ax           : subplot axes
    color        : color of the scatter points"""
    
    plot_style()
    ax.scatter(x,y,
                marker='o', s=150, color = color)
    ax.plot([0,1], [0,1], color='k')
    annotate_scatter_statistics(statistics=statistics, ax=ax)
    
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(subfig_label, fontweight='bold')


# %%
def annotate_scatter_statistics(statistics, ax):
    """ This is taken from pyaerocom. It is included in the 
    pyaerocom.plot.plotscatter.plot_scatter function.
    Annoation box for statistical properties in scatter plots
    
    Parameters
    ------------
    statistics : statistical values
    ax         : axes on which the box should be plotted"""
    ## position for statistics in scatter plot
    xypos =   {'var_info'       :   (0.01, .95),
                   'refdata_mean'   :   (0.01, 0.90),
                   'data_mean'      :   (0.01, 0.86),
                   'nmb'            :   (0.01, 0.82),
                   'mnmb'           :   (0.35, 0.82),
                   'R'              :   (0.01, 0.78),
                   'rms'            :   (0.50, 0.78),
                   'R_kendall'      :   (0.01, 0.74),
                   'fge'            :   (0.50, 0.74),
                   'ts_type'        :   (0.8, 0.1),
                   'filter_name'    :   (0.8, 0.06)}

    ax.annotate('Mean (x-data): {:.3f}'.format(statistics['refdata_mean']),
                        xy=xypos['refdata_mean'], xycoords='axes fraction', 
                        fontsize=20, 
                        color='red')
    ax.annotate('Mean (y-data): {:.3f}'.format(statistics['data_mean']),
                        xy=xypos['data_mean'], xycoords='axes fraction', 
                        fontsize=20, 
                        color='red')
    ax.annotate('R (Pearson): {:.3f}'.format(statistics['R']),
                        xy=xypos['R'], xycoords='axes fraction', 
                        fontsize=20, 
                        color='red')
    ax.annotate('RMS: {:.3f}'.format(statistics['rms']),
                        xy=xypos['rms'], xycoords='axes fraction', 
                        fontsize=20, 
                        color='red')
    ax.annotate('R (Kendall): {:.3f}'.format(statistics['R_kendall']),
                        xy=xypos['R_kendall'], xycoords='axes fraction', 
                        fontsize=20, 
                        color='red')
    ax.annotate('FGE: {:.1f}'.format(statistics['fge']),
                        xy=xypos['fge'], xycoords='axes fraction', 
                        fontsize=20, 
                        color='red')


# %%
def plt_seasonal_model_ensemble(xarray, ax,  starty, endy, color=None,
                                label = None):
    """This creates a plot of the AOD seasonal variability and shades the area
    of uncertainty.
    
    Parameters
    ------------
    xarray       : xarray holding the AOD data
    ax           : subplot axes
    starty       : string of analysis begin
    endy         : string of analysis end
    color        : color of the lines"""
    plot_style()
    
    # plot the median
    l, = xarray['median_'+starty+endy].plot(ax = ax, color =color, linewidth = 3,label=label)
    ax.fill_between(xarray['median_'+starty+endy].month,
                    xarray['median_'+starty+endy] - xarray['std_'+starty+endy],
                    xarray['median_'+starty+endy] + xarray['std_'+starty+endy],
                    alpha=0.3, facecolor =color)
    
    return(l)


# %%
def plt_zonal_model_merra(ax,cmip,cmip_std,merra_zonal_median, 
                          merra_zonal_std,model, color=None):
    """This creates a plot of the zonal averaged AOD and shades the area 
    of uncertainty.
    
    Parameters
    ------------
    ax                : subplot axes
    cmip              : median of the CMIP6 model
    cmip_std          : standard deviation of the CMIP6 model
    merra_zonal_median: median of the chosen MERRA2 
    merra_zonal_std   : standar deviation of the chosen MERRA2
    model             : name of th CMIP6 model
    color             : color of the title"""
    plot_style()
    cmip.mean(['month'],keep_attrs=True).plot(ax=ax, linewidth=3)
    ax.fill_between(cmip.mean(['month'],keep_attrs=True).lat,
                    cmip.mean(['month'],keep_attrs=True) - cmip_std.mean(['month'],keep_attrs=True),
                    cmip.mean(['month'],keep_attrs=True) + cmip_std.mean(['month'],keep_attrs=True),
                    alpha=0.3,)
 #   merra_zonal.plot(ax = ax, linewidth=3,color='k')
    
    
    ax.set_title(model, color=color,fontweight='bold')

# %%
