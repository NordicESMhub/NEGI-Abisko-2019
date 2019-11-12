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

from imports import *

def custom_plot(x,y):
    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot(x,y)
    ax.set_title('Example Plot')
    ax.set_ylabel('y label')
    ax.set_xlabel('x label')
    ax.grid()
    return ax

def mydateparser(x):
    if 'nan' in x:
        return(" ")
    else:
        return pd.datetime.strptime(x, "%Y %m %d %H %M")

# a
def average_aero_data(filenm, monthavg = True):
    '''
    This function takes a filepath as an argument, and assumes the format described in:
    shared-ns1000k/inputs/Aerosol_sizedist_obs/Readme.txt
    A pandas data from containing monthly averages is returned.
    '''
#    mydateparser = lambda x: pd.datetime.strptime(x, "%Y %m %d %H %M")
    
    data = pd.read_csv(filenm,  parse_dates=[['0', '0.1', '0.2', '0.3', '0.4']], date_parser = mydateparser, na_values = ['NaN', '-999', 'nan', '-1'])
    data = data.dropna(axis = 0)
    data.rename(columns={'0_0.1_0.2_0.3_0.4':'date'}, inplace = True)
    #data.head()

    data = data.set_index('date')

    data.replace(to_replace=-999, value = np.nan, inplace=True)

    # Remove last column
    data.drop(labels='0.6', axis=1, inplace=True)

    if monthavg == True: # allow monthly averages to be decided
        monthly = data.resample('M').mean() #.mean().plot()
        return monthly
    else:
        return data
    
def converttoN(filenm):
    '''
    Convert aerosol size distribution data from dN/dlog(Dp) to N
    '''
    cp = filenm.copy()
    radii = cp.columns[1:] # First column is a different format ??
    newcols = []
    for i,diams in enumerate(radii): # For each column, convert to units of N
        diamfl = np.float(diams)
        if i >= len(radii) - 1: # Exception for the last case
            colrange = str(diams) + '-' + str(diamfl + 50)
            factor = np.log10((diamfl + 50) / diamfl)
        else:
            colrange = diams + '-' + str(radii[i+1])
            ratio = np.float(radii[i+1]) / diamfl
            factor = np.log10(ratio)
        cp[colrange] = cp[diams] * factor # Create new column 
        newcols.append(colrange) # Save column name to a list
    
    small = newcols[:8] # 20-50nm
    med = newcols[8:14] # 50-100nm
    large = newcols[14:] # 100-550nm
    cp['20-50 nm'] = cp[small].sum(axis=1)
    cp['50-100 nm'] = cp[med].sum(axis=1)
    cp['100-500 nm'] = cp[large].sum(axis=1)
    cp['all_aero'] = cp[newcols].sum(axis=1)
   
    return cp

def select_from_netcdf(netcdf_path, var, lev_ind = None, date_range = None, time_avg = None):
    '''
    This function will take a file path, the variable of interest, 
    and optional variable ranges, and return files data from these selections. 
    Future work could have two dictionary arguments for sel and isel function
    arguments. And could easily include multiple variables.
    date_range is a tuple (start_date, end_date)
    '''
    temp_data = xr.open_dataset(netcdf_path)[var]  # open the dataset, select the variable
    # The order matters here if you apply an averaging.
    if lev_ind != None: # if an elevation parameter has been passed
        temp_data = temp_data.isel(lev=lev_ind)
    if date_range != None: # if a date range has been passed
        temp_data = temp_data.sel(time=slice(date_range[0], date_range[1])) # Select 
    if time_avg != None:
        temp_data = temp_data.groupby(time_avg).mean() # Create averages, this can be slow
    
    return temp_data

def select_loc_to_pandas(dataset, coords):
    '''
    This function takes an xarray dataset and a (lat, lon) coordinate iterable.
    It selects the data for the location and returns a pandas datafram object.
    '''
    _xr_ds = xr.Dataset() # empty xarray Dataset
    for vals in dataset:
        _da = dataset[vals]        
        _da = _da.sel(lat=coords[0], lon=coords[1], method='nearest')
        _xr_ds[vals]=_da
    _df = _xr_ds.to_dataframe()
    return _df

def myfunc(): # using a function to test the autoreload settings.
    print('heyhey')
    
def just_values(array_like, digits = None): 
    '''
    Simple function to strip unrelated values from an xarray object. Will optionally round.
    '''
    
    if digits != None:
        return np.round(np.float(array_like), digits)    
    
    else:
        return np.float(array_like) 
