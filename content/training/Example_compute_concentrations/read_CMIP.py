import pandas as pd
import sys
#sys.path.append('negi-stuff/') # insert path to negi-stuff if not installed. 
from negi_stuff.modules.imps import np,xr
from negi_stuff.modules import cmip6
from negi_stuff.modules import zarray, make_folders
import json
import os
import glob


def load_model_y(model, var_name, from_y, to_y, chunks={'time':5},
                 experiment='historical', piCont_nr_years=30):
    """
    Opens file containing required years (does not slice)
    
    model: model name
    var_name: variable name (full)
    from_y: from which year
    to_y: to which year
    chunks: chunks
    experiment : which class of experiments
    returns: ds: containing required years, real: the realisation it found
    """
    print('%s: Loading %s'%(model,var_name))
    # get filelist :
    files, real =  get_filelist(model, var_name, from_y, to_y, 
                                experiment=experiment, piCont_nr_years=piCont_nr_years)
    # sort the filelist so years are in right order
    files.sort()
    #str_from = '%04d'%from_y
    #str_to = '%04d'%to_y
    ds= xr.open_mfdataset(files,combine='by_coords', chunks=chunks)
    return ds, real

def get_filelist(model, var_name, from_y, to_y, experiment='historical', piCont_nr_years=30):
    """
    Picks out the files to load a variable (var_name) from some year (from_y) 
    to some other year (to_y) for the right experiment. 
    Will pick the first realisation it finds. 
    Special case included for piControl. It will pick the first x (set by piCont_nr_years)
    """
    real = 'LABEL'
    t_s = 'TIME START'
    t_e = 'TIME END'
    f_p = 'FILE_PATH'
    # Search for variable:
    df = cmip6.search_cmip6(var_name+'_*', model=model, experiment=experiment)
    # pick out realisation list
    realizations = list(df[real].unique())
    # sort the list:
    realizations.sort()
    _df = df.sort_values(by=real)
    lab = realizations[0] # pick out first realisation
    # very crude an ugly way of avoiding picking r10 before r1:
    notDone=True
    i=1
    while notDone:
        #print(lab)
        if lab[2] in ['%s'%ii for ii in np.arange(10)]:
            if len(_df)>i:
                lab=realizations[i]#, real]
                i+=1
            else: notDone=False
        else:
            notDone=False
    _df2 = _df[_df[real]==lab]
    
    ## Check if start_year unique:
    _df2 = _df2[_df2['FREQUENCY']=='mon']
    _df2.loc[:,t_e]=pd.to_numeric(_df2[t_e])#[float(_df2.loc[ii, t_s])]
    _df2.loc[:,t_s]=pd.to_numeric(_df2[t_s])#[float(_df2.loc[ii, t_s])]
    # Special case for piControl:
    if experiment=='piControl':
        from_y = int(_df2[t_s].min()/100)
        to_y = from_y + piCont_nr_years
    # pick out the files for specified years:
    _df2 = _df2[_df2[t_e]>from_y*100]
    _df2 = _df2[_df2[t_s]<to_y*100]
    ## Check if start_year unique:
    _df2 = _df2.drop_duplicates(subset=t_s)
    _df2 = _df2.drop_duplicates(subset=t_e)
    _df2 = _df2.sort_values(by=t_s)
    # Check if first file contains everything we need:
    ff_dt =(_df2[t_e].values[0]-_df2[t_s].values[0])/100
    if ff_dt>=(to_y-from_y):
        files = [_df2[f_p].values[0]]#.iloc[0]]
    else:
        files = list(_df2[f_p])
    
    print(files)
    return files, lab

def load_model_y_save(model, varL, from_y, to_y, experiment='historical', outdir='sliced_dt/', bottom_lev=False, piCont_nr_years=30):
    """
    Loads, slices and saves specified nr of years from model and vars
    model: str, model name
    varL: list of variables to load
    from_y: from which year the data should be sliced
    to_y: to which year the data should be sliced
    """
    li= []

    for var_name in varL:
        # load data
        _ds, real = load_model_y(model, var_name, from_y, to_y, experiment=experiment, piCont_nr_years=piCont_nr_years)
        # slica the data
        if experiment=='piControl': # take x first years
            _ds = _ds.isel(time=slice(0, 12*piCont_nr_years))
        else: #take specified years
            str_from = '%04d'%(from_y+1)
            str_to = '%04d'%to_y
            _ds= _ds.sel(time=slice(str_from, str_to))
        # if only bottom lev:
        if bottom_lev:
            if 'lev' in _ds[var_name].dims:
                _ds = _ds.isel(lev=0)
                lev=0
            else: lev=None
        else: lev=None
        # get the out file name: 
        filen=outdir+'/' + calc_filen(model, var_name, from_y, to_y, experiment, realisation= real, lev=lev)
        # only save is file not already saved (saves us a lot of time)
        if not os.path.isfile(filen):
            # make the folders so we can make the file:
            make_folders(filen)
            try:
                _ds.to_netcdf(filen)#
                _ds.close()
            # One exception for CESM models:
            except Exception as e:# ValueError:
                if 'CESM2' in model:
                    try:
                        encoding={var_name:{'_FillValue':1e+20}}
                        _ds.to_netcdf(filen,encoding=encoding)
                        _ds.close()
                    except:
                        print(e)
                        print('Coulnt save %s %s %s' %(model, var_name,filen))
                        return _ds
                else:
                    print(e)
                    print('Coulnt save %s %s %s' %(model, var_name,filen))
                    return _ds
    
def load_model_y_lev_save(model, varL, from_y, to_y, experiment='historical', lev=0, savedir='sliced_dt/'):
    li= []
    for var_name in varL:
        _ds = load_model_y(model, var_name, from_y, to_y, experiment=experiment)
        if 'lev' in _ds[var_name].dims:
            _ds = _ds.isel(lev=lev)
        path = savedir + calc_filen(model, var_name, from_y, to_y, experiment, lev=lev)
        make_folders(path)
        _ds.to_netcdf(path)

def calc_filen(model, var, from_y, to_y, experiment, lev=None, realisation='', statistic=''):
    """
    Makes default filenames. Useful for getting the files for loading. 
    """
    n = '%s/%s%s_%s_%s_%s_%s_%s'%(model,statistic,  var,model, experiment, realisation,  from_y, to_y )
    if experiment=='piControl':
    
        n = '%s/%s%s_%s_%s_%s_first30y'%(model,statistic,  var,model, experiment, realisation)#,  from_y, to_y )
        
    if lev is not None:
        n=n+'_lev%s'%lev
    n=n+'.nc'
    return n
def get_fn_real_wildcard(basedir, model, var, from_y, to_y, experiment, lev=None, realisation='*', statistic=''):
    fn = calc_filen(model, var, from_y, to_y, experiment, lev='*', realisation=realisation, statistic='')
    print(basedir + fn.replace('_lev', '*'))#[0]
    return glob.glob(basedir+fn.replace('_lev', '*'))[0]
    

def clean_ds_for_save(ds: {xr.Dataset, xr.DataArray}, check_variables=False):
    """
    Clean xarray ds or da for saving. Replace booleans with 'True'/'False'
    :type ds: xr.Dataset, xr.DataArray
    :param ds: xarray to be "cleaned"
    :param check_variables:
    :return: ds cleaned
    """
    attrs = ds.attrs.copy()
    for at in attrs:
        ds.attrs[at] =_bool2str(ds.attrs[at])
        ds.attrs[at] =_is_none(ds.attrs[at])
        if type(attrs[at]) is dict:
            del ds.attrs[at]

    if check_variables and type(ds) is xr.Dataset:
        for var in ds.variables:
            for at in ds.variables.attrs:
                ds[var].attrs[at] = _bool2str(ds[var].attrs[at])
                ds[var].attrs[at] = _is_none(ds[var].attrs[at])

    return ds


def _bool2str(_a):
    if type(_a) is bool:
        if _a: return 'True'
        else: return 'False'
    else: return _a

def _is_none(_a):
    if _a is None:
        return 'None'
    else:
        return _a



def make_folders(path):
    """
    Takes path and creates to folders
    :param path: Path you want to create (if not already existant)
    :return: nothing

    Example (want to make folders for placing file myfile.png:
    >>> path='my/folders/myfile.png'
    >>> make_folders(path)
    """
    path = extract_path_from_filepath(path)
    split_path = path.split('/')
    if (path[0] == '/'):

        path_inc = '/'
    else:
        path_inc = ''
    for ii in range(0,len(split_path)):
        # if ii==0: path_inc=path_inc+split_path[ii]
        path_inc = path_inc + split_path[ii]
        if not os.path.exists(path_inc):
            os.makedirs(path_inc)
        path_inc = path_inc + '/'

    return

def extract_path_from_filepath(file_path):
    """
    ex: 'folder/to/file.txt' returns 'folder/to/'
    :param file_path:
    :return:
    """

    st_ind=file_path.rfind('/')
    foldern = file_path[0:st_ind]+'/'
    return foldern