
from sverchok.dependencies import SvDependency

ex_dependencies = dict()

try:
    import sverchok

    from sverchok.dependencies import (
            SvDependency,
            ensurepip,
            pip, scipy, geomdl, skimage,
            mcubes, circlify,
            FreeCAD
        )

    sverchok_d = ex_dependencies["sverchok"] = SvDependency('Sverchok', "https://github.com/nortikin/sverchok")
    sverchok_d.module = sverchok
except ImportError:
    message =  "Sverchok addon is not available. Sverchok-GIS will not work."
    print(message)
    sverchok = None

# pygalmesh_d = ex_dependencies["pygalmesh"] = SvDependency("pygalmesh", "https://github.com/nschloe/pygalmesh")
# try:
#     import pygalmesh
#     pygalmesh_d.module = pygalmesh
# except ImportError:
#     pygalmesh = None

geopandas_d = ex_dependencies["geopandas"] = SvDependency("geopandas", "https://github.com/geopandas/geopandas")
try:
    import geopandas
    geopandas_d.module = geopandas
except ImportError:
    geopandas = None

