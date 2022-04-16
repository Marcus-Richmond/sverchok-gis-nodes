
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
from pathlib import Path
import nodeitems_utils
import bl_operators

import sverchok
from sverchok.core import sv_registration_utils #, make_node_list
from sverchok.utils import auto_gather_node_classes, get_node_class_reference
from sverchok.menu import SverchNodeItem, node_add_operators, SverchNodeCategory, register_node_panels, unregister_node_panels, unregister_node_add_operators
from sverchok.utils.extra_categories import register_extra_category_provider, unregister_extra_category_provider
from sverchok.ui.nodeview_space_menu import make_extra_category_menus, layout_draw_categories
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, zip_long_repeat
from sverchok.utils.logging import info, debug

DOCS_LINK = ''
MODULE_NAME = "sverchok_gis"

# make sverchok the root module name, (if sverchok dir not named exactly "sverchok")
if __name__ != MODULE_NAME:
    sys.modules[MODULE_NAME] = sys.modules[__name__]

import sverchok_gis
from sverchok_gis import icons, settings, sockets, examples, menu
from sverchok_gis.nodes_index import nodes_index
from sverchok_gis.utils import show_welcome


def make_node_list():
    modules = []
    base_name = "sverchok_gis.nodes"
    index = nodes_index()
    for category, items in index:
        for module_name, node_name in items:
            if node_name == 'separator':
                continue
            module = importlib.import_module(f".{module_name}", base_name)
            modules.append(module)
    return modules

def plain_node_list():
    node_cats = {}
    index = nodes_index()
    for category, items in index:
        nodes = []
        for _, node_name in items:
            nodes.append([node_name])
        node_cats[category] = nodes
    return node_cats

imported_modules = [icons] + make_node_list()

reload_event = False

if "bpy" in locals():
    reload_event = True
    info("Reloading sverchok-gis...")
    reload_modules()

import bpy

def register_nodes():
    node_modules = make_node_list()
    for module in node_modules:
        module.register()
    info("Registered %s nodes", len(node_modules))

def unregister_nodes():
    global imported_modules
    for module in reversed(imported_modules):
        module.unregister()

def make_categories():
    menu_cats = []
    index = nodes_index()
    for category, items in index:
        identifier = "SVERCHOK_GIS_" + category.replace(' ', '_')
        node_items = []
        for item in items:
            nodetype = item[1]
            rna = get_node_class_reference(nodetype)
            if not rna and nodetype != 'separator':
                info("Node `%s' is not available (probably due to missing dependencies).", nodetype)
            else:
                node_item = SverchNodeItem.new(nodetype)
                node_items.append(node_item)
        if node_items:
            cat = SverchNodeCategory(
                        identifier,
                        category,
                        items=node_items
                    )
            menu_cats.append(cat)
    return menu_cats

def add_nodes_to_sv():
    index = nodes_index()
    for _, items in index:
        for item in items:
            nodetype = item[1]
            rna = get_node_class_reference(nodetype)
            if not rna and nodetype != 'separator':
                info("Node `%s' is not available (probably due to missing dependencies).", nodetype)
            else:
                SverchNodeItem.new(nodetype)



node_cats = plain_node_list()



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
    global gis_menu_classes  # ?

    debug("Registering sverchok-gis")

    settings.register()
    icons.register()
    sockets.register()

    register_nodes()
    extra_nodes = importlib.import_module(".nodes", "sverchok_gis")
    auto_gather_node_classes(extra_nodes)

    add_nodes_to_sv()
    menu.register()

    cats_menu = make_categories() # This would load every sverchok-open3d category straight in the Sv menu

    menu_category_provider = SvGISCategoryProvider("SVERCHOK_GIS", cats_menu, DOCS_LINK, use_custom_menu=True, custom_menu='NODEVIEW_MT_GIS')
    register_extra_category_provider(menu_category_provider)
    examples.register()

    # with make_categories() This would load every sverchok-open3d category straight in the Sv menu
    # gis_menu_classes = make_extra_category_menus()

    show_welcome()

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
    #unregister_node_add_operators()
    unregister_nodes()

    menu.unregister()
    icons.unregister()
    sockets.unregister()
    settings.unregister()
