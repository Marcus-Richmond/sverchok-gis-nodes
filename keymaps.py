# keymaps.py

nodeview_keymaps = []


def add_keymap():
    import bpy
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')
        kmi = km.keymap_items.new('wm.call_menu', 'L', 'PRESS', shift=True)
        kmi.properties.name = "NODEVIEW_MT_GIS"
        nodeview_keymaps.append((km, kmi))

def remove_keymap():

    for km, kmi in nodeview_keymaps:
        try:
            km.keymap_items.remove(kmi)
        except Exception as e:
            err = repr(e)
            if "cannot be removed from 'Node Editor'" in err:
                print('keymaps for Node Editor already removed by another add-on, sverchok will skip this step in unregister')
                break

    nodeview_keymaps.clear()


def register():
    add_keymap()


def unregister():
    remove_keymap()