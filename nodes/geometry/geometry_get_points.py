import bpy
from sverchok.utils.dummy_nodes import add_dummy
from sverchok_gis.dependencies import geopandas as gpd
import sverchok_gis

if gpd is None:

    add_dummy('SvSGNImportGeometryPoint', 'Triangle Mesh Clean', 'geopandas')

else:

    # import pandas as pd
    # import fiona

    from sverchok.node_tree import SverchCustomTreeNode
    from sverchok.data_structure import updateNode

    class SvSGNImportGeometryPoint(SverchCustomTreeNode, bpy.types.Node):
        """
        Triggers: GIS import
        Tooltip: Import GPKG point layer
        """
        bl_idname = 'SvSGNImportGeometryPoint'  # should be add to `sverchok/index.md` file
        bl_label = 'Import Point Geometry'
        bl_icon = 'RNA'

        def sv_init(self, context):  # All socket types are in `sverchok/core/sockets.py` file
            # inputs
            self.inputs.new('SvFilePathSocket', "GPKG Path")
            self.inputs.new('SvStringsSocket', "Layer Name")
            
            # outputs
            self.outputs.new('SvVerticesSocket', "Vertices")

        def process(self):  
            # create initial variables      
            self.path = self.inputs["GPKG Path"].sv_get(deepcopy = False)
            self.layername = self.inputs["Layer Name"].sv_get(deepcopy = False)        
            
            if self.path and self.layername:
                self.layername = str(self.layername[0][0])

                # read in gpkg layer as geopandas data frame
                gpd1 = gpd.read_file(str(self.path[0][0]), layer = self.layername)

                # call geo interface method on geodataframe
                gi = gpd1.__geo_interface__

                # create empty lists to add new vertices to
                Vertices_features_individual = []

                # determine how many dimensions are stored in coordinates
                coordinate_length = len(gi['features'][0]['geometry']['coordinates'])

                # for loop to create vertices
                if coordinate_length == 3:
                    for feature in gi['features']:
                        x, y, z = feature['geometry']['coordinates']
                        Vertices_features_individual.append([x,y,z])
                elif coordinate_length == 2:
                    for feature in gi['features']:
                        x, y = feature['geometry']['coordinates']
                        Vertices_features_individual.append([x,y,0])

                Vertices = [Vertices_features_individual]
                
                
            self.outputs["Vertices"].sv_set(Vertices)
            
classes = [SvSGNImportGeometryPoint]
register, unregister = sverchok_gis.utils.register_class_factory_deps(classes, deps=[gpd])            

# def register():
#     if gpd is not None:
#         bpy.utils.register_class(SvSGNImportGeometryPoint)

# def unregister():
#     if gpd is not None:    
#         bpy.utils.unregister_class(SvSGNImportGeometryPoint)
