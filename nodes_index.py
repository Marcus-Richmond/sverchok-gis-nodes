def nodes_index():
    return [
    ("General", [
        ("general.o3d_import", "SvO3ImportNode"),
        ("general.o3d_export", "SvO3ExportNode")]),
    ("Geometry", [
        ("geometry.point_cloud_in", "SvO3PointCloudInNode"),
        ("geometry.point_cloud_out", "SvO3PointCloudOutNode"),
        ("geometry.point_cloud_downsample", "SvO3PointCloudDownSampleNode")])
    ]
