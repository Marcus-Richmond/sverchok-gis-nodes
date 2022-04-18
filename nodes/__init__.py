import importlib
import sverchok_gis
from sverchok.utils import auto_gather_node_classes
from sverchok.utils.logging import info, debug

# __init__.py
def register():
    from sverchok_gis.utils._load_addon_architecture import make_node_list, add_nodes_to_sv

    node_modules = make_node_list()
    for module in node_modules:
        module.register()
    info("Registered %s nodes", len(node_modules))

    extra_nodes = importlib.import_module(".nodes", "sverchok_gis")
    auto_gather_node_classes(extra_nodes)
    add_nodes_to_sv()


def unregister():
    from sverchok_gis import imported_modules
    for module in reversed(imported_modules):
        module.unregister()