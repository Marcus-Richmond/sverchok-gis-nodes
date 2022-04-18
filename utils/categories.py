# categories.py
import nodeitems_utils
from sverchok_gis import DOCS_LINK
from sverchok_gis.utils._load_addon_architecture import SvGISCategoryProvider


def register():
    from sverchok.utils.extra_categories import register_extra_category_provider
    from sverchok_gis.utils._load_addon_architecture import make_categories

    cats_menu = make_categories()
    menu_category_provider = SvGISCategoryProvider("SVERCHOK_GIS", cats_menu, DOCS_LINK, use_custom_menu=True, custom_menu='NODEVIEW_MT_GIS')
    register_extra_category_provider(menu_category_provider)


def unregister():
    from sverchok.utils.extra_categories import unregister_extra_category_provider

    if 'SVERCHOK_GIS' in nodeitems_utils._node_categories:
        nodeitems_utils.unregister_node_categories("SVERCHOK_GIS")
    unregister_extra_category_provider("SVERCHOK_GIS")