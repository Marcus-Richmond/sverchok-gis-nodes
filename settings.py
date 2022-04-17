import sys
import bpy
from bpy.types import AddonPreferences

if bpy.app.version >= (2, 91, 0):
    PYPATH = sys.executable
else:
    PYPATH = bpy.app.binary_path_python

import sverchok_gis
from sverchok.dependencies import draw_message
from sverchok_gis.dependencies import ex_dependencies, pip, ensurepip
from sverchok.utils.context_managers import addon_preferences

COMMITS_LINK = 'https://api.github.com/repos/Marcus-Richmond/sverchok-gis-nodes/commits'
ADDON_NAME = sverchok_gis.__name__
ADDON_PRETTY_NAME = 'Sverchok GIS'
ARCHIVE_LINK = 'https://github.com/Marcus-Richmond/sverchok-gis-nodes/archive/'
MASTER_BRANCH_NAME = 'master'

def draw_in_sv_prefs(layout):
    draw_message(layout, "geo pandas", dependencies=ex_dependencies)
    
def update_addon_ui(layout):
    layout.operator('node.sv_show_latest_commits', text='Show Last Commits').commits_link = COMMITS_LINK
    with addon_preferences(ADDON_NAME) as prefs:

        if not prefs.available_new_version:
            check = layout.operator('node.sverchok_check_for_upgrades_wsha', text='Check for Upgrades')
            check.commits_link = COMMITS_LINK
            check.addon_name = ADDON_NAME
        else:
            update_op = layout.operator('node.sverchok_update_addon', text=f'Upgrade {ADDON_PRETTY_NAME}')
            update_op.addon_name = ADDON_NAME
            update_op.master_branch_name = MASTER_BRANCH_NAME
            update_op.archive_link = ARCHIVE_LINK

def sv_draw_gis_update_menu_in_panel(self, context):
    layout = self.layout
    box = layout.box()
    box.label(text=ADDON_PRETTY_NAME)
    update_addon_ui(box)

get_icon = lambda package: 'CANCEL' if not package else 'CHECKMARK'

class SvGISPreferences(AddonPreferences):
    """

    This section describes the UI area in the addon preferences panel.
    - which deps to install
    - potentially one-click to install
    - here we can offer links to further information about installing deps ( if user encounters issues )

    """
    bl_idname = __package__

    available_new_version: bpy.props.BoolProperty(default=False)
    dload_archive_name: bpy.props.StringProperty(name="archive name", default=MASTER_BRANCH_NAME) # default = "master"
    dload_archive_path: bpy.props.StringProperty(name="archive path", default=ARCHIVE_LINK)

    def draw(self, context):
        layout = self.layout
        box = layout.box()

        box.label(text="Dependencies:")
        draw_message(box, "sverchok", dependencies=ex_dependencies)
        # box.label(text="below is a list of python modules that need to be installed if you wish to use all gis nodes")
        # https://github.com/Marcus-Richmond/sverchok-gis-nodes/issues/7
        # draw_message(box, "pandas", dependencies=ex_dependencies)
        # draw_message(box, "gdal", dependencies=ex_dependencies)
        # draw_message(box, "fiona", dependencies=ex_dependencies)
        # draw_message(box, "geopandas", dependencies=ex_dependencies)
        # shapely?
        row = box.row()
        row.label(text="For now i recommend reading: ")
        row.operator('wm.url_open', text="sverchok-gis-nodes/issues/7").url = "https://github.com/Marcus-Richmond/sverchok-gis-nodes/issues/7"

        row = layout.row()
        row.operator('node.sv_show_latest_commits').commits_link = COMMITS_LINK

        if not self.available_new_version:
            check = row.operator('node.sverchok_check_for_upgrades_wsha', text='Check for Upgrades')
            check.commits_link = COMMITS_LINK
            check.addon_name = ADDON_NAME
        else:
            update_op = row.operator('node.sverchok_update_addon', text=f'Upgrade {ADDON_PRETTY_NAME}')
            update_op.addon_name = ADDON_NAME
            update_op.master_branch_name = MASTER_BRANCH_NAME
            update_op.archive_link = ARCHIVE_LINK

def register():
    bpy.utils.register_class(SvGISPreferences)
    bpy.types.SV_PT_SverchokUtilsPanel.append(sv_draw_gis_update_menu_in_panel)

def unregister():
    bpy.utils.unregister_class(SvGISPreferences)
    bpy.types.SV_PT_SverchokUtilsPanel.remove(sv_draw_gis_update_menu_in_panel)
