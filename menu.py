import bpy
from sverchok.ui.nodeview_space_menu import make_extra_category_menus, layout_draw_categories
from sv_gis_nodes.nodes_index import nodes_index
# from sv_gis_nodes.dependencies import open3d as o3d

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
    bl_label = "GIS"

    def draw(self, context):
        layout = self.layout
        # layout.operator_context = 'INVOKE_REGION_WIN'
        # if o3d is None:
        #     layout.operator('node.sv_ex_pip_install', text="Install Open3d Library with PIP").package = "open3d"
        # else:
        #     layout_draw_categories(self.layout, self.bl_label, node_cats['Utils'])
        #     layout.menu("NODEVIEW_MT_Open3DPointCloudMenu")
        #     layout.menu("NODEVIEW_MT_Open3DTriangleMeshMenu")
        # layout.menu("NODEVIEW_MT_Open3DPointCloudMenu")

# does not get registered
class NodeViewMenuTemplate(bpy.types.Menu):
    bl_label = ""
    def draw(self, context):
        layout_draw_categories(self.layout, self.bl_label, node_cats[self.bl_label])

def make_class(name, bl_label):
    name = 'NODEVIEW_MT_GIS' + name + 'Menu'
    clazz = type(name, (NodeViewMenuTemplate,), {'bl_label': bl_label})
    return clazz

menu_classes = [
    # make_class('PointCloud', 'Point Cloud'),
    # make_class('TriangleMesh', 'Triangle Mesh')
    ]

def register():
    for class_name in menu_classes:
        bpy.utils.register_class(class_name)
    bpy.utils.register_class(NODEVIEW_MT_GIS)

def unregister():
    bpy.utils.unregister_class(NODEVIEW_MT_GIS)
    for class_name in menu_classes:
        bpy.utils.unregister_class(class_name)


