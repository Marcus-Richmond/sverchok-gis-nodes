# mixin_debug_dict.py
import bpy
from sverchok.data_structure import node_id

class SvSGNDebugMixinDict():
    """
    the goal of this mixin is to abstract away the node_dict creation.
    user/node creator should be able to just assume a node dict will be created
    correctly, and reset if necessary.
    """
    sgn_debug_dict = dict()    # special kind of variable.
    sgn_debug_mode: bpy.types.BoolProperty(default=False, name="debug mode", description="debug switch for node")

    def get_current_debug_dict(self):
        self.n_id = node_id(self)
        found_dict = self.sgn_debug_dict.get(self.n_id)
        if not found_dict:
            print("recreated new dict")
            self.sgn_debug_dict[self.n_id] = {}
            found_dict = self.sgn_debug_dict[self.n_id]
        return found_dict

    def clear_current_debug_dict(self):
        self.n_id = node_id(self)
        self.sgn_debug_dict[self.n_id] = {}

    def set_debug_dict_new_pair(self, key_name, key_value):
        self.get_current_debug_dict()[key_name] = key_value
