from pathlib import Path

import bpy
from sverchok.ui.sv_examples_menu import add_extra_examples, make_submenu_classes
import sverchok_gis

EXAMPLES_PATH = Path(sverchok_gis.__file__).parent / 'json_examples'

def example_categories_names():
    for category_path in EXAMPLES_PATH.iterdir():
        if category_path.is_dir():
            yield (EXAMPLES_PATH, category_path.name)


def register():
    submenu_classes = (make_submenu_classes(path, category_name) for path, category_name in example_categories_names())
    for examples_menu in submenu_classes:
        bpy.utils.register_class(examples_menu)
    add_extra_examples('GIS', EXAMPLES_PATH)

def unregister():
    pass
