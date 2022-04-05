
bl_info = {
    "name": "Sverchok-GIS",
    "author": "Marcus Richmond",
    "version": (0, 1, 0, 0),
    "blender": (2, 81, 0),
    "location": "Node Editor",
    "category": "Node",
    "description": "Sverchok GIS Nodes",
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
from sverchok.data_structure import updateNode, zip_long_repeat
from sverchok.utils.logging import info, debug

# make sverchok the root module name, (if sverchok dir not named exactly "sverchok")
if __name__ != "sverchok_gis":
    sys.modules["sverchok_gis"] = sys.modules[__name__]

DOCS_LINK = ''
MODULE_NAME = 'geopandas'

def nodes_index():
    return [("import", [("import.import_attribute", "SvO3ImportAttributeNode")]),]

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

imported_modules = make_node_list()

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

def make_menu():
    menu = []
    index = nodes_index()
    for category, items in index:
        identifier = "SVERCHOK_GIS_" + category.replace(' ', '_')
        node_items = []
        for item in items:
            if not item:
                node_item = SverchSeparator()
                node_items.append(node_item)
                continue

            nodetype = item[1]
            rna = get_node_class_reference(nodetype)
            if not rna:
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
            menu.append(cat)
    return menu

class SvExCategoryProvider(object):
    def __init__(self, identifier, menu):
        self.identifier = identifier
        self.menu = menu

    def get_categories(self):
        return self.menu

our_menu_classes = []

def reload_modules():
    global imported_modules
    for im in imported_modules:
        debug("Reloading: %s", im)
        importlib.reload(im)


def register():
    global our_menu_classes

    debug("Registering sverchok-gis")

    register_nodes()
    extra_nodes = importlib.import_module(".nodes", "sverchok_gis")
    auto_gather_node_classes(extra_nodes)

    menu = make_menu()
    menu_category_provider = SvExCategoryProvider("SVERCHOK_GIS", menu)
    register_extra_category_provider(menu_category_provider) 

    our_menu_classes = make_extra_category_menus()


def unregister():
    global our_menu_classes
    if 'SVERCHOK_GIS' in nodeitems_utils._node_categories:
        #unregister_node_panels()
        nodeitems_utils.unregister_node_categories("SVERCHOK_GIS")
    for clazz in our_menu_classes:
        try:
            bpy.utils.unregister_class(clazz)
        except Exception as e:
            print("Can't unregister menu class %s" % clazz)
            print(e)
    unregister_extra_category_provider("SVERCHOK_GIS")
    #unregister_node_add_operators()
    unregister_nodes()
