def nodes_index():
    return [{"Extra": [                                                                 # Group menu name
                ({'icon_name': 'SV_EX_ROOT_ICON'}, ),                                   # icon image ID of Group menu name. Used only first elem of tuple
                {"GIS": [
                    ({'icon_name': 'SURFACE_DATA'}, ),             
                    ('import.import_gpkg_layer', 'SvSGNImportGPKGLayer')
                ]},
            ]}]