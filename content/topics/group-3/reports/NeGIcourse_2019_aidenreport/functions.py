# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # **NeGI Course 2019 in Abisko**
# ## **Supplementary material: functions used in report**
# #### Aiden Jönsson
#
# First, import the necessary packages:

from imports import (pd, np, xr, mpl, plt, cy, ccrs, pya)

# This function is used to plot the location of the AOD observations and the swath used for satellite versus model AOD comparisons:

def plotaodobs():
    dpi = 100
    resolution = '50m'
    plt.figure(figsize=(4,4))
    ortho = ccrs.Orthographic(central_longitude=-40, central_latitude=74)
    ax = plt.axes(projection=ortho)
    ax.coastlines(resolution='50m')
    ax.stock_img()
    ax.gridlines(color='white')
    x = [0,0,10,10]
    y = [78,74,74,78]
    geo = ccrs.Geodetic()
    ax.set_extent([-180, 360, 45, 90])
    ax.fill(x, y, color='orange', transform=geo, alpha=1)
    ax.annotate('Swath', xy=(-20,83), xycoords=ccrs.PlateCarree()._as_mpl_transform(ax), fontsize=18, color='orange')
    ax.scatter(16.1, 69.28, marker='o', c='r', transform=geo)
    ax.annotate('Andenes \n$69.28^{\circ}$ N \n$16.10^{\circ}$ W',xy=(-30,60),xycoords=ccrs.PlateCarree()._as_mpl_transform(ax),fontsize=16,color='red')

# This function is used to plot the locations of the two stations where the black carbon measurements were taken:

def plotbcobs():
    ## Define geolocations for the two stations
    ## Summit
    sumlat = 72.58
    sumlon = -38.48
    ## Alert
    alelat = 82.5
    alelon = -62.34
    dpi = 100
    resolution = '50m'
    plt.figure(figsize=(4,4))
    ortho = ccrs.Orthographic(central_longitude=sumlon, central_latitude=sumlat)
    ax = plt.axes(projection=ortho)
    ax.coastlines(resolution='50m')
    ax.stock_img()
    ax.gridlines(color='white')
    lons = [sumlon,alelon]
    lats = [sumlat,alelat]
    geo = ccrs.Geodetic()
    ax.set_extent([-180, 360, 45, 90])
    ax.scatter(lons, lats, marker='o', c='r', transform=geo)
    ax.annotate('Summit \n$72.58^{\circ}$ N, \n$38.48^{\circ}$ W', xy=(sumlon+4,sumlat-6), xycoords=ccrs.PlateCarree()._as_mpl_transform(ax), fontsize=16, color='red')
    ax.annotate('Alert \n$82.50^{\circ}$ N, \n$62.34^{\circ}$ W', xy=(alelon+0.5,alelat+1.1), xycoords=ccrs.PlateCarree()._as_mpl_transform(ax), fontsize=16, color='red')


# This function is used to open and plot modeled AOD versus satellite-observed AOD:

def retrieve_aod_data():
    ## Call satellite data
    ## Mean:
    ## ATSR
    path = '~/shared-ns1000k/dataporten-home/8dec3597-2d9337-2d41e5-2d9a21-2d71ca64bb7a8c/AOD_section/ATSR_hist_od550aer.nc'
    ds_atsr = xr.open_dataset(path)
    ## AATSR
    path = '~/shared-ns1000k/dataporten-home/8dec3597-2d9337-2d41e5-2d9a21-2d71ca64bb7a8c/AOD_section/AATSR_hist_od550aer.nc'
    ds_aatsr = xr.open_dataset(path)
    ## Standard deviation:
    ## ATSR
    path = '~/shared-ns1000k/dataporten-home/8dec3597-2d9337-2d41e5-2d9a21-2d71ca64bb7a8c/AOD_section/ATSR_sdev_od550aer.nc'
    dss_atsr = xr.open_dataset(path)
    ## AATSR
    path = '~/shared-ns1000k/dataporten-home/8dec3597-2d9337-2d41e5-2d9a21-2d71ca64bb7a8c/AOD_section/AATSR_sdev_od550aer.nc'
    dss_aatsr = xr.open_dataset(path)
    ## Rename the satellite datasets' lat/lon dimension names for ease of reading
    ds_atsr = ds_atsr.rename({'latitude':'lat','longitude':'lon'})
    ds_aatsr = ds_aatsr.rename({'latitude':'lat','longitude':'lon'})
    dss_atsr = dss_atsr.rename({'latitude':'lat','longitude':'lon'})
    dss_aatsr = dss_aatsr.rename({'latitude':'lat','longitude':'lon'})
    
    ## Call model data
    ## Mean:
    ## CanESM5
    path = '~/shared-ns1000k/dataporten-home/8dec3597-2d9337-2d41e5-2d9a21-2d71ca64bb7a8c/AOD_section/Can_hist_od550aer.nc'
    ds_can = xr.open_dataset(path)
    ## CESM2
    path = '~/shared-ns1000k/dataporten-home/8dec3597-2d9337-2d41e5-2d9a21-2d71ca64bb7a8c/AOD_section/CESM2_hist_od550aer.nc'
    ds_cesm = xr.open_dataset(path)
    ## NorESM2
    path = '~/shared-ns1000k/dataporten-home/8dec3597-2d9337-2d41e5-2d9a21-2d71ca64bb7a8c/AOD_section/NorESM_hist_od550aer.nc'
    ds_nor = xr.open_dataset(path)
    ## UKESM1
    path = '~/shared-ns1000k/dataporten-home/8dec3597-2d9337-2d41e5-2d9a21-2d71ca64bb7a8c/AOD_section/UKESM_hist_od550aer.nc'
    ds_uk = xr.open_dataset(path)
    ## CNRM
    path = '~/shared-ns1000k/dataporten-home/8dec3597-2d9337-2d41e5-2d9a21-2d71ca64bb7a8c/AOD_section/CNRM_hist_od550aer.nc'
    ds_cnrm = xr.open_dataset(path)
    ##Standard deviation:
    ## CanESM5
    path = '~/shared-ns1000k/dataporten-home/8dec3597-2d9337-2d41e5-2d9a21-2d71ca64bb7a8c/AOD_section/Can_sdev_od550aer.nc'
    dss_can = xr.open_dataset(path)
    ## CESM2
    path = '~/shared-ns1000k/dataporten-home/8dec3597-2d9337-2d41e5-2d9a21-2d71ca64bb7a8c/AOD_section/CESM2_sdev_od550aer.nc'
    dss_cesm = xr.open_dataset(path)
    ## NorESM2
    path = '~/shared-ns1000k/dataporten-home/8dec3597-2d9337-2d41e5-2d9a21-2d71ca64bb7a8c/AOD_section/NorESM_sdev_od550aer.nc'
    dss_nor = xr.open_dataset(path)
    ## UKESM1
    path = '~/shared-ns1000k/dataporten-home/8dec3597-2d9337-2d41e5-2d9a21-2d71ca64bb7a8c/AOD_section/UKESM_sdev_od550aer.nc'
    dss_uk = xr.open_dataset(path)
    ## CNRM
    path = '~/shared-ns1000k/dataporten-home/8dec3597-2d9337-2d41e5-2d9a21-2d71ca64bb7a8c/AOD_section/CNRM_sdev_od550aer.nc'
    dss_cnrm = xr.open_dataset(path)
    
    ##Define some constants for the variable names so that calling them is easier
    lat = 'lat'
    lon = 'lon'
    time = 'time'
    aod = 'od550aer' #aerosol optical depth
    
    ##Define slices for the box to retrieve satellite data from
    latbox = slice(74,78)
    lonbox = slice(0,10)
    
    ## Mean:
    _nor = ds_nor.sel(lat=latbox,lon=lonbox).mean(dim={lat,lon})
    _uk = ds_uk.sel(lat=latbox,lon=lonbox).mean(dim={lat,lon})
    _cnrm = ds_cnrm.sel(lat=latbox,lon=lonbox).mean(dim={lat,lon})
    _cesm = ds_cesm.sel(lat=latbox,lon=lonbox).mean(dim={lat,lon})
    _can = ds_can.sel(lat=latbox,lon=lonbox).mean(dim={lat,lon})
    _atsr = ds_atsr.sel(lat=latbox,lon=lonbox).mean(dim={lat,lon})
    _aatsr = ds_aatsr.sel(lat=latbox,lon=lonbox).mean(dim={lat,lon})
    
    ## Standard deviation:
    s_nor = ds_nor.sel(lat=latbox,lon=lonbox).mean(dim={lat,lon})
    s_uk = ds_uk.sel(lat=latbox,lon=lonbox).mean(dim={lat,lon})
    s_cnrm = ds_cnrm.sel(lat=latbox,lon=lonbox).mean(dim={lat,lon})
    s_cesm = ds_cesm.sel(lat=latbox,lon=lonbox).mean(dim={lat,lon})
    s_can = ds_can.sel(lat=latbox,lon=lonbox).mean(dim={lat,lon})
    s_atsr = ds_atsr.sel(lat=latbox,lon=lonbox).mean(dim={lat,lon})
    s_aatsr = ds_aatsr.sel(lat=latbox,lon=lonbox).mean(dim={lat,lon})
    
    ## Make an array list of months
    mon = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    
    ## Plotting model data
    f = plt.figure(figsize=(8,6))
    plt.errorbar(mon,_nor[aod],s_nor[aod],label='NorESM2-LM',capsize=5)
    plt.errorbar(mon,_uk[aod],s_uk[aod],label='UKESM1-0-LL',capsize=5)
    plt.errorbar(mon,_cnrm[aod],s_uk[aod],label='CNRM-ESM2',capsize=5)
    plt.errorbar(mon,_cesm[aod],s_cesm[aod],label='CESM2',capsize=5)
    plt.errorbar(mon,_can[aod],s_can[aod],label='CanESM5',color='pink',capsize=5)
    
    ## Plotting ATSR/AATSR data
    plt.errorbar(mon,_atsr[aod],s_atsr[aod],label='ATSR v4.3',linestyle='--',color='grey',capsize=5)
    plt.errorbar(mon,_aatsr[aod],s_aatsr[aod],label='AATSR v4.3',linestyle='--',color='black',capsize=5)
    plt.ylabel('AOD at 550 nm',fontsize=16)
    plt.legend(bbox_to_anchor=(1, 0.725))

# This function is used to plot black carbon measurements versus modeled:

## Retrieve black carbon model data:
def plot_bc_obsvsmodel(_summitbc,_alertbc):
    ## IPSL-CM6A-LR
    path = '~/shared-cmip6-for-ns1000k/historical/IPSL-CM6A-LR/r1i1p1f1/loadbc_Eday_IPSL-CM6A-LR_historical_r1i1p1f1_gr_18500101-20141231.nc'
    ds_ipsl = xr.open_dataset(path)
    ## CESM2
    path = '~/shared-cmip6-for-ns1000k/historical/CESM2/r1i1p1f1/loadbc_Eday_CESM2_historical_r1i1p1f1_gn_20100101-20150101.nc'
    ds_cesm = xr.open_dataset(path)
    ## CESM2-WACCM
    path = '~/shared-cmip6-for-ns1000k/historical/CESM2-WACCM/r1i1p1f1/loadbc_Eday_CESM2-WACCM_historical_r1i1p1f1_gn_20100101-20150101.nc'
    ds_waccm = xr.open_dataset(path)
    ## GFDL-CM4
    path = '~/shared-cmip6-for-ns1000k/historical/GFDL-CM4/r1i1p1f1/loadbc_Eday_GFDL-CM4_historical_r1i1p1f1_gr2_20100101-20141231.nc'
    ds_gfdl = xr.open_dataset(path)
    
    ## Define some variables to make it easier to call
    lat = 'lat'
    lon = 'lon'
    time = 'time'
    bc = 'loadbc' #black carbon loading
    mon = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'] #make a string of months to plot against
    
    ## Define geolocations for the two stations
    ## Summit
    sumlat = 72.58
    sumlon = -38.48
    ## Alert
    alelat = 82.5
    alelon = -62.34
    
    ## Select the two stations' data from the models (squeeze is used to reduce dimensions)
    ## For Summit
    ##Select grid box for the location
    sum_cesm = ds_cesm.sel(lat=sumlat,lon=sumlon,method='nearest').squeeze()
    sum_waccm = ds_waccm.sel(lat=sumlat,lon=sumlon,method='nearest').squeeze()
    sum_ipsl = ds_ipsl.sel(lat=sumlat,lon=sumlon,method='nearest').squeeze()
    sum_gfdl = ds_gfdl.sel(lat=sumlat,lon=sumlon,method='nearest').squeeze()
    ##Select the range 2010-2014
    sum_cesm = sum_cesm.sel(time=slice('2010-01-01','2014-12-31'))
    sum_waccm = sum_waccm.sel(time=slice('2010-01-01','2014-12-31'))
    sum_ipsl = sum_ipsl.sel(time=slice('2010-01-01','2014-12-31'))
    sum_gfdl = sum_gfdl.sel(time=slice('2010-01-01','2014-12-31'))
    ##Calculate the mean and standard deviation
    sum_cesm_mean = sum_cesm.groupby('time.month').mean()
    sum_cesm_std = sum_cesm.groupby('time.month').std()
    sum_waccm_mean = sum_waccm.groupby('time.month').mean()
    sum_waccm_std = sum_waccm.groupby('time.month').std()
    sum_ipsl_mean = sum_ipsl.groupby('time.month').mean()
    sum_ipsl_std = sum_ipsl.groupby('time.month').std()
    sum_gfdl_mean = sum_gfdl.groupby('time.month').mean()
    sum_gfdl_std = sum_gfdl.groupby('time.month').std()
    
    ## For Alert
    ##Select grid box for the location
    al_cesm = ds_cesm.sel(lat=alelat,lon=alelon,method='nearest').squeeze()
    al_waccm = ds_waccm.sel(lat=alelat,lon=alelon,method='nearest').squeeze()
    al_ipsl = ds_ipsl.sel(lat=alelat,lon=alelon,method='nearest').squeeze()
    al_gfdl = ds_gfdl.sel(lat=alelat,lon=alelon,method='nearest').squeeze()
    ##Select the range 2010-2014
    al_cesm = al_cesm.sel(time=slice('2010-01-01','2014-12-31'))
    al_waccm = al_waccm.sel(time=slice('2010-01-01','2014-12-31'))
    al_ipsl = al_ipsl.sel(time=slice('2010-01-01','2014-12-31'))
    al_gfdl = al_gfdl.sel(time=slice('2010-01-01','2014-12-31'))
    ##Calculate the mean and standard deviation
    al_cesm_mean = al_cesm.groupby('time.month').mean()
    al_cesm_std = al_cesm.groupby('time.month').std()
    al_waccm_mean = al_waccm.groupby('time.month').mean()
    al_waccm_std = al_waccm.groupby('time.month').std()
    al_ipsl_mean = al_ipsl.groupby('time.month').mean()
    al_ipsl_std = al_ipsl.groupby('time.month').std()
    al_gfdl_mean = al_gfdl.groupby('time.month').mean()
    al_gfdl_std = al_gfdl.groupby('time.month').std()   
    
    ## Plot the annual cycles together, two axes, with standard deviation bars for model data
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True,figsize=(16,5))

    ax1.plot(mon, _summitbc, linestyle='--', color='black', label='EBAS observed')
    ax1.set_ylabel('equivalent black carbon \n mass concentration [$\mu g/m^3$]',fontsize=14)
    ax12 = ax1.twinx()
    ax12.errorbar(mon,sum_cesm_mean[bc]*1e9,sum_cesm_std[bc]*1e9,label='CESM2',capsize=5)
    ax12.errorbar(mon,sum_waccm_mean[bc]*1e9,sum_waccm_std[bc]*1e9,label='CESM2-WACCM',capsize=5)
    ax12.errorbar(mon,sum_ipsl_mean[bc]*1e9,sum_ipsl_std[bc]*1e9,label='IPSL-CM6A-LR',capsize=5)
    ax12.errorbar(mon,sum_gfdl_mean[bc]*1e9,sum_gfdl_std[bc]*1e9,label='GFDL-CM4',capsize=5)
    ax12.set_ylabel('black carbon loading [$\mu g/m^2$]',fontsize=14)
    ax1.set_title('Summit, 2010 ($72.58^{\circ}$ N, $38.48^{\circ}$ W)', fontsize=15)
    
    ax2.plot(mon, _alertbc, linestyle='--', color='black', label='EBAS observed')
    ax2.set_ylabel('equivalent black carbon \n mass concentration [$\mu g/m^3$]',fontsize=14)
    ax22 = ax2.twinx()
    ax22.errorbar(mon,al_cesm_mean[bc]*1e9,al_cesm_std[bc]*1e9,label='CESM2',capsize=5)
    ax22.errorbar(mon,al_waccm_mean[bc]*1e9,al_waccm_std[bc]*1e9,label='CESM2-WACCM',capsize=5)
    ax22.errorbar(mon,al_ipsl_mean[bc]*1e9,al_ipsl_std[bc]*1e9,label='IPSL-CM6A-LR',capsize=5)
    ax22.errorbar(mon,al_gfdl_mean[bc]*1e9,al_gfdl_std[bc]*1e9,label='GFDL-CM4',capsize=5)
    ax22.set_ylabel('black carbon loading [$\mu g/m^2$]',fontsize=14)
    ax22.legend(bbox_to_anchor=(-0.14, 0.6))
    ax2.legend(bbox_to_anchor=(-0.145, 0.7))
    ax2.set_title('Alert, 2011-2012 ($82.50^{\circ}$ N, $62.34^{\circ}$ W)', fontsize=15)
    
    f.tight_layout()


# This function is used to plot the differences in surface temperatures between the PI-BC and PI-control experiments:

def plot_pibc_tas():
    ##NorESM
    path = '~/shared-ns1000k/dataporten-home/8dec3597-2d9337-2d41e5-2d9a21-2d71ca64bb7a8c/PIBC_experiment/NorESM2_pi-bc_tas.nc'
    ds_nor = xr.open_dataset(path)
    path = '~/shared-ns1000k/dataporten-home/8dec3597-2d9337-2d41e5-2d9a21-2d71ca64bb7a8c/PIBC_experiment/NorESM2_picontrol_tas.nc'
    dsc_nor = xr.open_dataset(path)
    ##UKESM
    path = '~/shared-ns1000k/dataporten-home/8dec3597-2d9337-2d41e5-2d9a21-2d71ca64bb7a8c/PIBC_experiment/UKESM1_pi-bc_tas.nc'
    ds_uk = xr.open_dataset(path)
    path = '~/shared-ns1000k/dataporten-home/8dec3597-2d9337-2d41e5-2d9a21-2d71ca64bb7a8c/PIBC_experiment/UKESM1_picontrol_tas.nc'
    dsc_uk = xr.open_dataset(path)
    ##CNRM
    path = '~/shared-ns1000k/dataporten-home/8dec3597-2d9337-2d41e5-2d9a21-2d71ca64bb7a8c/PIBC_experiment/CNRM_picontrol_tas.nc'
    dsc_cnrm = xr.open_dataset(path)
    path = '~/shared-ns1000k/dataporten-home/8dec3597-2d9337-2d41e5-2d9a21-2d71ca64bb7a8c/PIBC_experiment/CNRM_pi-bc_tas.nc'
    ds_cnrm = xr.open_dataset(path)
    
    ## Define some variable names so that calling them is easier
    lat = 'lat'
    lon = 'lon'
    time = 'time'
    tas = 'tas' #temperature at surface
    
    ## Calculate the differences between the experiment and the control run:
    nor_diff = ds_nor - dsc_nor
    uk_diff = ds_uk - dsc_uk
    cnrm_diff = ds_cnrm - dsc_cnrm
    
    ## We can choose different seasons to visualize:
    _nor_sum = nor_diff[tas][{time:2}]
    _uk_sum = uk_diff[tas][{time:2}]
    _cnrm_sum = cnrm_diff[tas][{time:2}]
    _nor_win = nor_diff[tas][{time:0}]
    _uk_win = uk_diff[tas][{time:0}]
    _cnrm_win = cnrm_diff[tas][{time:0}]
    
    ## Plot the fields
    f = plt.figure(figsize=(10,7))
    
    ax1 = plt.subplot(231,projection=cy.crs.NorthPolarStereo())
    ax1.set_extent((-180, 180, 60, 90), crs=cy.crs.PlateCarree())
    ax1.gridlines()
    ax1.coastlines()
    ax1.set_title('NorESM2-LM (DJF)')
    cb = _nor_win.plot(ax=ax1,transform=ccrs.PlateCarree(),clim=(-0.1,0.01),add_colorbar=False,add_labels=False,vmin=-2.5,vmax=2.5,cmap='bwr')
    
    ax2 = plt.subplot(232,projection=cy.crs.NorthPolarStereo())
    ax2.set_extent((-180, 180, 60, 90), crs=cy.crs.PlateCarree())
    ax2.gridlines()
    ax2.coastlines()
    ax2.set_title('UKESM1-0-LL (DJF)')
    _uk_win.plot(ax=ax2,transform=ccrs.PlateCarree(),clim=(-0.01,0.01),add_colorbar=False,add_labels=False,vmin=-2.5,vmax=2.5,cmap='bwr')
    
    ax3 = plt.subplot(233,projection=cy.crs.NorthPolarStereo())
    ax3.set_extent((-180, 180, 60, 90), crs=cy.crs.PlateCarree())
    ax3.gridlines()
    ax3.coastlines()
    ax3.set_title('CNRM-ESM2 (DJF)')
    _cnrm_win.plot(ax=ax3,transform=ccrs.PlateCarree(),clim=(-0.01,0.01),add_colorbar=False,add_labels=False,vmin=-2.5,vmax=2.5,cmap='bwr')
    
    ax4 = plt.subplot(234,projection=cy.crs.NorthPolarStereo())
    ax4.set_extent((-180, 180, 60, 90), crs=cy.crs.PlateCarree())
    ax4.gridlines()
    ax4.coastlines()
    ax4.set_title('NorESM2-LM (JJA)')
    _nor_sum.plot(ax=ax4,transform=ccrs.PlateCarree(),clim=(-0.01,0.01),add_colorbar=False,add_labels=False,vmin=-2.5,vmax=2.5,cmap='bwr')
    
    ax5 = plt.subplot(235,projection=cy.crs.NorthPolarStereo())
    ax5.set_extent((-180, 180, 60, 90), crs=cy.crs.PlateCarree())
    ax5.gridlines()
    ax5.coastlines()
    ax5.set_title('UKESM1-0-LL (JJA)')
    _uk_sum.plot(ax=ax5,transform=ccrs.PlateCarree(),clim=(-0.01,0.01),add_colorbar=False,add_labels=False,vmin=-2.5,vmax=2.5,cmap='bwr')
    
    ax6 = plt.subplot(236,projection=cy.crs.NorthPolarStereo())
    ax6.set_extent((-180, 180, 60, 90), crs=cy.crs.PlateCarree())
    ax6.gridlines()
    ax6.coastlines()
    ax6.set_title('CNRM-ESM2 (JJA)')
    _cnrm_sum.plot(ax=ax6,transform=ccrs.PlateCarree(),clim=(-0.1,0.1),add_colorbar=False,add_labels=False,vmin=-2.5,vmax=2.5,cmap='bwr')
    
    f.subplots_adjust(right=0.88)
    cbar_ax = f.add_axes([0.9, 0.15, 0.01, 0.7])
    f.colorbar(cb, cax=cbar_ax)
    cbar_ax.set_ylabel('$\Delta T$ [K]')


# This function is used to plot the differences in AOD between the PI-BC and PI-control experiments:

def plot_pibc_aod():
    ##NorESM
    path = '~/shared-ns1000k/dataporten-home/8dec3597-2d9337-2d41e5-2d9a21-2d71ca64bb7a8c/PIBC_experiment/NorESM2_diff_od550aer.nc'
    nor_diff = xr.open_dataset(path)
    ##UKESM
    path = '~/shared-ns1000k/dataporten-home/8dec3597-2d9337-2d41e5-2d9a21-2d71ca64bb7a8c/PIBC_experiment/UKESM1_diff_od550aer.nc'
    uk_diff = xr.open_dataset(path)
    ##CNRM
    path = '~/shared-ns1000k/dataporten-home/8dec3597-2d9337-2d41e5-2d9a21-2d71ca64bb7a8c/PIBC_experiment/CNRM_diff_od550aer.nc'
    cnrm_diff = xr.open_dataset(path)
    
    ## Define some variable names so that calling them is easier
    lat = 'lat'
    lon = 'lon'
    time = 'time'
    aod = 'od550aer' #aerosol optical depth
    
    ## We can choose different seasons to visualize:
    _nor_sum = nor_diff[aod][{time:2}]
    _uk_sum = uk_diff[aod][{time:2}]
    _cnrm_sum = cnrm_diff[aod][{time:2}]
    _nor_win = nor_diff[aod][{time:0}]
    _uk_win = uk_diff[aod][{time:0}]
    _cnrm_win = cnrm_diff[aod][{time:0}]
    
    ## Plot the fields
    f = plt.figure(figsize=(10,7))
    
    ax1 = plt.subplot(231,projection=cy.crs.NorthPolarStereo())
    ax1.set_extent((-180, 180, 60, 90), crs=cy.crs.PlateCarree())
    ax1.gridlines()
    ax1.coastlines()
    ax1.set_title('NorESM2-LM (DJF)')
    cb = _nor_win.plot(ax=ax1,transform=ccrs.PlateCarree(),clim=(-0.01,0.01),add_colorbar=False,add_labels=False,vmin=-0.025,vmax=0.025,cmap='bwr')
    
    ax2 = plt.subplot(232,projection=cy.crs.NorthPolarStereo())
    ax2.set_extent((-180, 180, 60, 90), crs=cy.crs.PlateCarree())
    ax2.gridlines()
    ax2.coastlines()
    ax2.set_title('UKESM1-0-LL (DJF)')
    _uk_win.plot(ax=ax2,transform=ccrs.PlateCarree(),clim=(-0.01,0.01),add_colorbar=False,add_labels=False,vmin=-0.025,vmax=0.025,cmap='bwr')
    
    ax3 = plt.subplot(233,projection=cy.crs.NorthPolarStereo())
    ax3.set_extent((-180, 180, 60, 90), crs=cy.crs.PlateCarree())
    ax3.gridlines()
    ax3.coastlines()
    ax3.set_title('CNRM-ESM2 (DJF)')
    _cnrm_win.plot(ax=ax3,transform=ccrs.PlateCarree(),clim=(-0.01,0.01),add_colorbar=False,add_labels=False,vmin=-0.025,vmax=0.025,cmap='bwr')
    
    ax4 = plt.subplot(234,projection=cy.crs.NorthPolarStereo())
    ax4.set_extent((-180, 180, 60, 90), crs=cy.crs.PlateCarree())
    ax4.gridlines()
    ax4.coastlines()
    ax4.set_title('NorESM2-LM (JJA)')
    _nor_sum.plot(ax=ax4,transform=ccrs.PlateCarree(),clim=(-0.01,0.01),add_colorbar=False,add_labels=False,vmin=-0.025,vmax=0.025,cmap='bwr')
    
    ax5 = plt.subplot(235,projection=cy.crs.NorthPolarStereo())
    ax5.set_extent((-180, 180, 60, 90), crs=cy.crs.PlateCarree())
    ax5.gridlines()
    ax5.coastlines()
    ax5.set_title('UKESM1-0-LL (JJA)')
    _uk_sum.plot(ax=ax5,transform=ccrs.PlateCarree(),add_colorbar=False,add_labels=False,vmin=-0.025,vmax=0.025,cmap='bwr')
    
    ax6 = plt.subplot(236,projection=cy.crs.NorthPolarStereo())
    ax6.set_extent((-180, 180, 60, 90), crs=cy.crs.PlateCarree())
    ax6.gridlines()
    ax6.coastlines()
    ax6.set_title('CNRM-ESM2 (JJA)')
    _cnrm_sum.plot(ax=ax6,transform=ccrs.PlateCarree(),add_colorbar=False,add_labels=False,vmin=-0.025,vmax=0.025,cmap='bwr')
    
    f.subplots_adjust(right=0.88)
    cbar_ax = f.add_axes([0.9, 0.15, 0.01, 0.7])
    f.colorbar(cb, cax=cbar_ax)
    cbar_ax.set_ylabel('$\Delta AOD$')
