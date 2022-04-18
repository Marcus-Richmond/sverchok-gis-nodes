bl_info = {
    "name": "Sverchok-GIS",
    "author": "Various",
    "version": (0, 1, 0, 0),
    "blender": (3, 1, 0),
    "location": "Node Editor",
    "category": "Node",
    "description": "GIS nodes for Sverchok using geopandas",
    "warning": "Under heavy development",
    "wiki_url": "",
    "tracker_url": ""
}

import sys
import importlib
import sverchok
from sverchok.utils.logging import info, debug


DOCS_LINK = ''
MODULE_NAME = "sverchok_gis"

# make sverchok the root module name, (if sverchok dir not named exactly "sverchok")
if __name__ != MODULE_NAME:
    sys.modules[MODULE_NAME] = sys.modules[__name__]

import sverchok_gis
from sverchok_gis import icons, settings, sockets, examples, menu, nodes
from sverchok_gis.utils import show_welcome, categories
from sverchok_gis.utils._load_addon_architecture import make_node_list, plain_node_list
from sverchok_gis.utils._load_addon_architecture import register_all, unregister_all


imported_modules = [icons] + make_node_list()

reload_event = False
if "bpy" in locals():
    reload_event = True
    info("Reloading sverchok-gis...")
    reload_modules()

import bpy

node_cats = plain_node_list()

def reload_modules():
    global imported_modules
    for im in imported_modules:
        debug(f"Reloading: {im}")
        importlib.reload(im)


def register():
    debug("Registering sverchok-gis")
    register_all([settings, icons, sockets, nodes, menu, categories, examples])
    show_welcome()

def unregister():
    unregister_all([categories, nodes, menu, icons, sockets, settings])
