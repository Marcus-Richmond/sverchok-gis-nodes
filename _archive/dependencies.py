
from sverchok.dependencies import SvDependency

ex_dependencies = dict()

try:
    import sverchok
    from sverchok.utils.logging import info, error, debug

    from sverchok.dependencies import (
            SvDependency,
            ensurepip,
            pip, scipy, geomdl, skimage,
            mcubes, circlify,
            FreeCAD
        )

    sverchok_d = ex_dependencies["sverchok"] = SvDependency(None, "https://github.com/nortikin/sverchok")
    sverchok_d.module = sverchok
    sverchok_d.message =  "Sverchok addon is available"
except ImportError:
    message =  "Sverchok addon is not available. Sverchok-Open3d will not work."
    print(message)
    sverchok = None

geopandas_d = ex_dependencies["geopandas"] = SvDependency("geopandas", "https://geopandas.org/en/stable/")
geopandas_d.pip_installable = True
try:
    import geopandas
    geopandas_d.message = "geopandas package is available"
    geopandas_d.module = geopandas
except ImportError:
    geopandas_d.message = "geopandas package is not available, the addon will not work"
    info(geopandas_d.message)
    geopandas = None
