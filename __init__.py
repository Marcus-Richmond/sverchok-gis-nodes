
bl_info = {
    "name": "Sverchok-GIS-Nodes",
    "author": "Marcus Richmond",
    "version": (0, 1, 0, 0),
    "blender": (3, 1, 0),
    "location": "Node Editor",
    "category": "Node",
    "description": "Sverchok-GIS-Nodes",
    "warning": "",
    "wiki_url": "",
    "tracker_url": ""
}



import sys
import importlib
from pathlib import Path
import nodeitems_utils
import bl_operators

import sverchok
from sverchok.core import sv_registration_utils, make_node_list
from sverchok.utils import auto_gather_node_classes, get_node_class_reference
from sverchok.menu import SverchNodeItem, node_add_operators, SverchNodeCategory, register_node_panels, unregister_node_panels, unregister_node_add_operators
from sverchok.utils.extra_categories import register_extra_category_provider, unregister_extra_category_provider
from sverchok.ui.nodeview_space_menu import make_extra_category_menus, layout_draw_categories
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.utils.logging import info, debug

# make sverchok the root module name, (if sverchok dir not named exactly "sverchok")
if __name__ != "sv_gis_nodes":
    sys.modules["sv_gis_nodes"] = sys.modules[__name__]

import sv_gis_nodes
from sv_gis_nodes.bootstrapping import make_node_list
from sv_gis_nodes.ui import menu
# from sv_gis_nodes import menu
# from sv_gis_nodes.nodes_index import nodes_index
# from sverchok_open3d.utils import show_welcome

DOCS_LINK = 'https://github.com/vicdoval/sverchok-gis-nodes/tree/master/utils'
MODULE_NAME = 'sv_gis_nodes'


imported_modules = make_node_list()

reload_event = False

if "bpy" in locals():
    reload_event = True
    info("Reloading sv_gis_nodes...")
    reload_modules()

import bpy
from sv_gis_nodes.nodes_index import nodes_index


class SvGISCategoryProvider(object):
    def __init__(self, identifier, cats_menu, docs_link, use_custom_menu=False, custom_menu=None):
        self.identifier = identifier
        self.menu = cats_menu
        self.docs = docs_link
        self.use_custom_menu = use_custom_menu
        self.custom_menu = custom_menu

    def get_categories(self):
        return self.menu

gis_menu_classes = []

def reload_modules():
    global imported_modules
    for im in imported_modules:
        debug("Reloading: %s", im)
        importlib.reload(im)


def register():
    global gis_menu_classes

    debug("Registering sv_gis_nodes!")

    register_nodes()
    extra_nodes = importlib.import_module(".nodes", "sv_gis_nodes")
    auto_gather_node_classes(extra_nodes)

    add_nodes_to_sv()
    
    from sv_gis_nodes import menu
    menu.register()

    cats_menu = make_categories()

    menu_category_provider = SvGISCategoryProvider("SVERCHOK_GIS", cats_menu, DOCS_LINK, use_custom_menu=True, custom_menu='NODEVIEW_MT_GIS')
    register_extra_category_provider(menu_category_provider) #if 'SVERCHOK_OPEN3D' in nodeitems_utils._node_categories:


def unregister():
    global gis_menu_classes
    if 'SVERCHOK_GIS' in nodeitems_utils._node_categories:
        #unregister_node_panels()
        nodeitems_utils.unregister_node_categories("SVERCHOK_GIS")
    for clazz in gis_menu_classes:
        try:
            bpy.utils.unregister_class(clazz)
        except Exception as e:
            print("Can't unregister menu class %s" % clazz)
            print(e)
    unregister_extra_category_provider("SVERCHOK_GIS")
    unregister_nodes()
    menu.unregister()


