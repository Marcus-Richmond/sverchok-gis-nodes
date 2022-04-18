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
import nodeitems_utils

import sverchok
# from sverchok.core import sv_registration_utils #, make_node_list
from sverchok.utils import auto_gather_node_classes
from sverchok.utils.logging import info, debug
from sverchok.utils.extra_categories import register_extra_category_provider 
from sverchok.utils.extra_categories import unregister_extra_category_provider
from sverchok.ui.nodeview_space_menu import layout_draw_categories

DOCS_LINK = ''
MODULE_NAME = "sverchok_gis"

# make sverchok the root module name, (if sverchok dir not named exactly "sverchok")
if __name__ != MODULE_NAME: sys.modules[MODULE_NAME] = sys.modules[__name__]

import sverchok_gis
from sverchok_gis import icons, settings, sockets, examples, menu, nodes
from sverchok_gis.nodes_index import nodes_index
from sverchok_gis.utils import show_welcome
from sverchok_gis.utils._load_addon_architecture import make_node_list, plain_node_list
from sverchok_gis.utils._load_addon_architecture import register_all, unregister_all
from sverchok_gis.utils._load_addon_architecture import SvGISCategoryProvider

imported_modules = [icons] + make_node_list()

reload_event = False
if "bpy" in locals():
    reload_event = True
    info("Reloading sverchok-gis...")
    reload_modules()

import bpy
from sverchok_gis.utils._load_addon_architecture import make_categories, add_nodes_to_sv

node_cats = plain_node_list()

def reload_modules():
    global imported_modules
    for im in imported_modules:
        debug("Reloading: %s", im)
        importlib.reload(im)


def register():

    debug("Registering sverchok-gis")
    register_all([settings, icons, sockets, nodes])
    extra_nodes = importlib.import_module(".nodes", "sverchok_gis")
    auto_gather_node_classes(extra_nodes)

    add_nodes_to_sv()
    menu.register()

    cats_menu = make_categories() # This would load every sverchok-open3d category straight in the Sv menu

    menu_category_provider = SvGISCategoryProvider("SVERCHOK_GIS", cats_menu, DOCS_LINK, use_custom_menu=True, custom_menu='NODEVIEW_MT_GIS')
    register_extra_category_provider(menu_category_provider)
    examples.register()

    show_welcome()

def unregister():

    if 'SVERCHOK_GIS' in nodeitems_utils._node_categories:
        nodeitems_utils.unregister_node_categories("SVERCHOK_GIS")

    unregister_extra_category_provider("SVERCHOK_GIS")
    unregister_all([nodes, menu, icons, sockets, settings])
