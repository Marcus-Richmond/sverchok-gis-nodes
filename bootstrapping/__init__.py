import sys
import importlib

import sverchok
from sverchok.menu import SverchNodeItem
from sverchok.utils.logging import info, debug

import sv_gis_nodes
from sv_gis_nodes.nodes_index import nodes_index


def make_node_list():
    modules = []
    base_name = "sv_gis_nodes.nodes"
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
    from sv_gis_nodes import imported_modules
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

def reload_modules():
    from sv_gis_nodes import imported_modules
    for im in imported_modules:
        debug("Reloading: %s", im)
        importlib.reload(im)
