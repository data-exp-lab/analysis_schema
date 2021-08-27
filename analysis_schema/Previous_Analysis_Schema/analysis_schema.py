# -*- coding: utf-8 -*-

"""Main module."""

from pydantic import BaseModel

from .data_objects import DataObject, DataSource
from .dataset import (CosmologyContext, Dataset, DomainContext,
                      NeuroImagingContext, TurbulentContext)
from .fields import FieldDefinition
from .image_gallery import ImageGallery, PlotDefinition
from .operations import Average, Integrate, Maximum, Minimum, Operation, Sum
from .products import Profile, ProfileND, Projection
from .quantities import (Path, UnitfulArray, UnitfulCoordinate, UnitfulValue,
                         Vector)
from .stream_frontend import (AMRDataSpecification, AMRGridDataSpecification,
                              YTDatasetSpecification)
from .visualization_objects import (FixedResolutionBuffer, PhasePlot,
                                    PhasePlotMPL, ProfilePlot)

schema = {
    n: v
    for n, v in locals().items()
    if isinstance(v, type) and issubclass(v, BaseModel)
}
