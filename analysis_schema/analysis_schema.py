# -*- coding: utf-8 -*-

"""Main module."""

from pydantic import BaseModel

from .data_objects import Sphere, SphereID, Region, RegionID, AllData, AllDataID

from .dataset import (
    DomainContext,
    CosmologyContext,
    TurbulentContext,
    NeuroImagingContext,
    Dataset,
)

from .operations import Average, Sum, Minimum, Maximum, Integrate, Operation

from .products import Projection, ProfileND, Profile

from .quantities import UnitfulValue, UnitfulArray, UnitfulCoordinate, Vector, Path

from .visualization_objects import (
    FixedResolutionBuffer,
    ProfilePlot,
    PhasePlot,
    PhasePlotMPL,
)

from .fields import FieldDefinition

from .stream_frontend import (
    AMRGridDataSpecification,
    AMRDataSpecification,
    YTDatasetSpecification,
)

from .image_gallery import ImageGallery

schema = {
    n: v
    for n, v in locals().items()
    if isinstance(v, type) and issubclass(v, BaseModel)
}
