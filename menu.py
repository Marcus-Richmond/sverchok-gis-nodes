import bpy
from sverchok.ui.nodeview_space_menu import make_extra_category_menus, layout_draw_categories
from sverchok_gis.nodes_index import nodes_index
from sverchok_gis.dependencies import geopandas as gpd

def plain_node_list():
    node_categories = {}
    index = nodes_index()
    for category, items in index:
        nodes = []
        for _, node_name in items:
            nodes.append([node_name])
        node_categories[category] = nodes
    return node_categories

node_cats = plain_node_list()

class NODEVIEW_MT_GIS(bpy.types.Menu):
    bl_label = "GIS Menu"

    def draw(self, context):
        layout = self.layout

        layout.operator_context = 'INVOKE_REGION_WIN'
        if gpd is None:

            layout.operator('node.sv_ex_pip_install', text="Install geopandas Library with PIP").package = "geopandas"
        else:
            # layout_draw_categories(self.layout, self.bl_label, node_cats['Utils'])
            layout.menu("NODEVIEW_MT_GISGeneralMenu")
            layout.menu("NODEVIEW_MT_GISGeometryMenu")


# does not get registered
class NodeViewMenuTemplate(bpy.types.Menu):
    bl_label = ""
    def draw(self, context):
        layout_draw_categories(self.layout, self.bl_label, node_cats[self.bl_label])

def make_class(name, bl_label):
    return type(f'NODEVIEW_MT_GIS{name}Menu', (NodeViewMenuTemplate,), {'bl_label': bl_label})

menu_classes = [
    make_class('General', 'General'),
    make_class('Geometry', 'Geometry'),
    NODEVIEW_MT_GIS
]

register, unregister = bpy.utils.register_classes_factory(menu_classes)

