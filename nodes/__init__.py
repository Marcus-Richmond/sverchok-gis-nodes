import sverchok_gis
from sverchok.utils.logging import info, debug

# __init__.py
def register():
    from sverchok_gis.utils._load_addon_architecture import make_node_list

    node_modules = make_node_list()
    for module in node_modules:
        module.register()
    info("Registered %s nodes", len(node_modules))

def unregister():
    from sverchok_gis import imported_modules
    for module in reversed(imported_modules):
        module.unregister()