# gis_loader.py

import bpy
import sverchok
import sverchok_gis
from sverchok_gis.dependencies import geopandas as gpd

def get_loader():
    """
    the node shouldn't have to worry about whether or not the library is present.
    """
    if gpd is None:
        return None
    else:
        return gpd.read_file
