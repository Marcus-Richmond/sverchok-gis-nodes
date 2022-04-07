# node_1.py


# This file is part of project Sverchok. It's copyrighted by the contributors
# recorded in the version control history of the file, available from
# its original location https://github.com/nortikin/sverchok/commit/master
#  
# SPDX-License-Identifier: GPL3
# License-Filename: LICENSE

import bpy
# import mathutils
# from mathutils import Vector
# from bpy.props import FloatProperty, BoolProperty
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

class SvGISNode2(bpy.types.Node, SverchCustomTreeNode):
    
    """
    Triggers: SvGISNode2
    Tooltip: 
    
    A short description for reader of node code
    """

    bl_idname = 'SvGISNode2'
    bl_label = 'SvGISNode2'
    bl_icon = 'GREASEPENCIL'

    def sv_init(self, context):
        ...

    def draw_buttons(self, context, layout):
        ...

    def process(self):
        ...


classes = [SvGISNode2]
register, unregister = bpy.utils.register_classes_factory(classes)
