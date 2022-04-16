
import os
import numpy as np

from sverchok.utils.math import inverse, inverse_square, inverse_cubic

def show_welcome():
    text = r"""

  ________  .___    _________
 /  _____/  |   |  /   _____/
/   \  ___  |   |  \_____  \ 
\    \_\  \ |   |  /        \   nodes for Sverchok
 \______  / |___| /_______  /
        \/                \/ 
    initialized.

"""
    can_paint = os.name in {'posix'}

    with_color = "\033[1;31m{0}\033[0m" if can_paint else "{0}"
    for line in text.splitlines():
        print(with_color.format(line))


def registration_class_factory_deps(classes, deps=None):
    """
    usage
    from sverchok_gis.utils import registration_class_factory_deps

    classes = [SvSGNImportGeometryLine]
    register, unregister = sverchok.utils.registration_class_factory_deps(classes, deps=[gpd])

    """

    import bpy
    def register():
        if all(deps):
            _ = [bpy.utils.register_class(c) for c in classes]

    def unregister():
        if all(deps):
            _ = [bpy.utils.unregister_class(c) for c in classes]

    return register, unregister


