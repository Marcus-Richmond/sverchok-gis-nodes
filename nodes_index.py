def nodes_index():
    return [
    ("General", [
        ("general.general_load_gis_data", "SvSGNLoadGISData")]),
    ("Geometry", [
        ("geometry.geometry_get_points",     "SvSGNImportGeometryPoint"),
        ("geometry.geometry_get_lines",      "SvSGNImportGeometryLine"),
        ("geometry.geometry_get_polygons",   "SvSGNImportGeometryPolygon")]),
    ("Attribute", [
        ("general.general_import_attribute", "SvSGNImportAttribute"),
        ("general.general_import_attribute_as_dictionary", "SvSGNImportAttributeDict"),
        ("general.general_import_attribute_as_list", "SvSGNImportAttributeList"),
        ("general.general_get_keys_and_values", "SvSGNGetKeysAndValues")])
    ]



# def nodes_index():
#     """
#     provides automated collection of nodes_index, the downside is that this is sorted alphabetically
#     and may not ultimately reflect the ideal UI. You can use this to generate a hardcoded list too.
#     """
#     import sverchok_gis
#     from sverchok_gis import nodes

#     index_tuples = []
#     for folder in ["General", "Geometry"]:
#         section_list = []
#         folder_module = getattr(nodes, folder.lower())
#         nodefile_names = [nf_name for nf_name in dir(folder_module) if not nf_name.startswith("__")]
#         for nf in nodefile_names:
#             node_module = getattr(folder_module, nf)
#             class_name = node_module.classes[0].__name__
#             entry_tuple = (f"{folder.lower()}.{nf}", class_name)
#             section_list.append(entry_tuple)
#         index_tuples.append(tuple((folder, section_list)))

#     return index_tuples
