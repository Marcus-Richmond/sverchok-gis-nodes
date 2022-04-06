
bl_info = {
    "name": "Sverchok-GIS-Nodes",
    "author": "Marcus Richmond",
    "version": (0, 1, 0, 0),
    "blender": (2, 8, 0),
    "location": "Node Editor",
    "category": "Node",
    "description": "Sverchok-GIS-Nodes",
    "warning": "",
    "wiki_url": "",
    "tracker_url": ""
}

import sys
import os, re
from sys import platform
import bpy
blenderVersion =  "Blender"+str(bpy.app.version[0])+str(bpy.app.version[1])

# sitePackagesFolderName = os.path.join(os.path.dirname(os.path.realpath(__file__)), "site-packages")
# sverchokgisnodesFolderName = [filename for filename in os.listdir(sitePackagesFolderName) if filename.startswith("sverchok_gis_nodes")][0]
# sverchokgisnodesPath = os.path.join(sitePackagesFolderName, sverchokgisnodesFolderName)
# sys.path.append(sverchokgisnodesPath)
# sverchokgisnodesPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "site-packages")
# sys.path.append(sverchokgisnodesPath)

import importlib
import nodeitems_utils
import bl_operators
import sverchok
from sverchok.core import sv_registration_utils, make_node_list
from sverchok.utils import auto_gather_node_classes, get_node_class_reference
from sverchok.menu import SverchNodeItem, node_add_operators, SverchNodeCategory, register_node_panels, unregister_node_panels, unregister_node_add_operators
from sverchok.utils.extra_categories import register_extra_category_provider, unregister_extra_category_provider
from sverchok.ui.nodeview_space_menu import make_extra_category_menus, make_class, layout_draw_categories
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, zip_long_repeat
from sverchok.utils.logging import info, debug



# make sverchok the root module name, (if sverchok dir not named exactly "sverchok")

if __name__ != "sverchok-gis-nodes":
    sys.modules["sverchok-gis-nodes"] = sys.modules[__name__]

def nodes_index():
	coreNodes = [
                ("SverchokGISNodes.import_attribute", "SvSGNImportAttribute")
                ]
	return [("SverchokGISNodes", coreNodes)]

def make_node_list():
    modules = []
    base_name = "sverchok-gis-nodes.nodes"
    index = nodes_index()
    for category, items in index:
        for module_name, node_name in items:
            module = importlib.import_module(f".{module_name}", base_name)
            modules.append(module)
    return modules

imported_modules = make_node_list()

reload_event = False

def register_nodes():
	node_modules = make_node_list()
	for module in node_modules:
		module.register()
	#info("Registered %s nodes", len(node_modules))

def unregister_nodes():
	global imported_modules
	for module in reversed(imported_modules):
		module.unregister()

def make_menu():
    menu = []
    index = nodes_index()
    for category, items in index:
        identifier = "SVERCHOK-GIS-NODES_" + category.replace(' ', '_')
        node_items = []
        for item in items:
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

sverchok_gis_nodes_menu_classes = []


class NODEVIEW_MT_AddSGNSubcategoryImport(bpy.types.Menu):
    bl_label = "SGNSubcategoryImport"
    bl_idname = 'NODEVIEW_MT_AddSGNSubcategoryImport'

    def draw(self, context):
        layout = self.layout
        layout_draw_categories(self.layout, self.bl_label, [
            ['SvSGNImportAttribute']
        ])

make_class('SGNSubcategoryImport', 'SGN @ Import')

   
# Main menu
class NODEVIEW_MT_EX_SGN_sgn(bpy.types.Menu):
    bl_label = 'SverchokGISNodes'

    def draw(self, context):
        layout_draw_categories(self.layout, 'SverchokGISNodes', [
            ['@ Import']
        ])

def register():
    global sverchok_gis_nodes_menu_classes

    #debug("Registering Topologic")

    #settings.register()
    #icons.register()
    #sockets.register()
    bpy.utils.register_class(NODEVIEW_MT_EX_SGN_sgn)
    register_nodes()
    extra_nodes = importlib.import_module(".nodes", "sverchokgisnodes")
    auto_gather_node_classes(extra_nodes)
    bpy.utils.register_class(NODEVIEW_MT_AddSGNSubcategoryImport)
    menu = make_menu()
    menu_category_provider = SvExCategoryProvider("SGN", menu)
    register_extra_category_provider(menu_category_provider)
    nodeitems_utils.register_node_categories("SGN", menu)

def unregister():
    global topologic_menu_classes
    if 'SGN' in nodeitems_utils._node_categories:
        #unregister_node_panels()
        nodeitems_utils.unregister_node_categories("SGN")
    for clazz in topologic_menu_classes:
        try:
            bpy.utils.unregister_class(clazz)
        except Exception as e:
            print("Can't unregister menu class %s" % clazz)
            print(e)
    unregister_extra_category_provider("SGN")
    unregister_nodes()
    bpy.utils.unregister_class(NODEVIEW_MT_AddSGNSubcategoryImport)
    #sockets.unregister()
    #icons.unregister()
    #settings.unregister()
