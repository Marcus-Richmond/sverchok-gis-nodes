# _load_addon_architecture.py
import importlib

import sverchok
import sverchok_gis
from sverchok.utils.logging import info, debug
from sverchok.utils import get_node_class_reference
from sverchok.menu import SverchNodeItem, SverchNodeCategory
from sverchok_gis.nodes_index import nodes_index

def register_all(modules_in):
    for module in modules_in:
        module.register()

def unregister_all(modules_in):
    for module in modules_in:
        module.unregister()


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
                info(f"Node '{nodetype}' is not available (probably due to missing dependencies).")
            else:
                node_item = SverchNodeItem.new(nodetype)
                node_items.append(node_item)
        
        if node_items:
            cat = SverchNodeCategory(identifier, category, items=node_items)
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


class SvGISCategoryProvider(object):
    def __init__(self, identifier, cats_menu, docs_link, use_custom_menu=False, custom_menu=None):
        self.identifier = identifier
        self.menu = cats_menu
        self.docs = docs_link
        self.use_custom_menu = use_custom_menu
        self.custom_menu = custom_menu

    def get_categories(self):
        return self.menu


