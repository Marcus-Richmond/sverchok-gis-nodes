
import sys
import subprocess

import bpy
from bpy.types import AddonPreferences

if bpy.app.version >= (2, 91, 0):
    PYPATH = sys.executable
else:
    PYPATH = bpy.app.binary_path_python

from sverchok.dependencies import draw_message
from sverchok_gis.dependencies import ex_dependencies, pip, ensurepip

class SvGISPreferences(AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout

        def get_icon(package):
            if package is None:
                return 'CANCEL'
            else:
                return 'CHECKMARK'

        box = layout.box()

        box.label(text="Dependencies:")
        draw_message(box, "sverchok", dependencies=ex_dependencies)
        draw_message(box, "geopandas", dependencies=ex_dependencies)


def register():
    bpy.utils.register_class(SvGISPreferences)


def unregister():
    bpy.utils.unregister_class(SvGISPreferences)

if __name__ == '__main__':
    register()
