import xarray as xr
import numpy as np
import pandas as pd


def size_dist_to_xarray(loaded_ebas_file, step=2 ):
    filedata = loaded_ebas_file
    all_d = filedata.data[:,2:-1:step]
    time =  list(filedata.time_stamps)
    ds = xr.Dataset({'time':time})

    ds['sized'] = xr.DataArray(
        all_d, 
        dims={'time':ds['time'], 
              'd_index': np.arange(len(all_d[0,:]))}
    )
    return ds['sized']




# Get data for diameters within 20-50nm
def lognorm_to_concentration(data, start_col, end_col, start_date, end_date):
    df_sizes = data.loc[start_col:end_col,start_date:end_date].T

# Integrate over log10(Dp) to get Ntot
    Ntot = pd.Series(np.trapz(df_sizes,
    x = np.log10(df_sizes.columns)),
    index=df_sizes.index.copy())
    
    return Ntot




def load_seaice_xarray(filepath, shift_lons=True):
    import iris, xarray
    cube = iris.load_cube(DATA_DIR + FILE)
    if shift_lons:
        cube = cube.intersection(longitude=(-180, 180))
    return xarray.DataArray.from_iris(cube)
