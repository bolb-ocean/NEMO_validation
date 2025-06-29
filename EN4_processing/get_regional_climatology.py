### work in progress ###
### replication of  EN4_processing/map_profiles.py
### purpose > make gridded version of en4 data?

from PythonEnvCfg.config import config, bounds

cfg = config() # initialise variables in python

from dask.diagnostics import ProgressBar
import xarray as xr
import pandas as pd
import os

class regional_climatology(object):

    def __init__(self):

        # File paths 
        self.fn_out = cfg.dn_out + "surface_maps/"
        
        # Make out directory
        print(os.popen(f"mkdir -p {cfg.dn_out}").read())
        
    def get_season_bias(self):
        """ get seasonal regional bias """

        # get data
        path = cfg.dn_out + f"profiles/profiles_by_region_and_season.nc"
        self.season_ds = xr.open_dataset(path, chunks="auto")


    def restrict_to_surface(self, depth_lim=5, save=True):
        """ restrict to top x-metres """

        # set bounds
        bounds = [0,depth_lim]

        # sel is faster than where
        self.season_ds = self.season_ds.swap_dims({"z_dim":"depth"})
        self.season_ds = self.season_ds.sel(depth=bounds, method="nearest")

        # average
        self.season_ds = self.season_ds.mean("depth")

    def save_ds(self, ds, path):
        """ save data to path """

        with ProgressBar():
            ds.to_netcdf(self.fn_out + path)

def save_surface_EN4_bias_by_region_and_season():
    sc = regional_climatology()
    sc.get_season_bias()
    sc.restrict_to_surface()
    sc.save_ds(sc.season_ds, "near_surface_EN4_bias_by_season_by_region.nc")

save_full_depth_EN4_bias_by_region_and_season()
