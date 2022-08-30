import enum
from typing import Dict, List, Tuple, Union

from pydantic import BaseModel, Field

from .data_objects import DataSource
from .fields import FieldName
from .operations import ReturnsUnitfulValue
from .products import Projection
from .quantities import UnitfulCoordinate, UnitfulValue


class CenteringTypeEnum(str, enum.Enum):
    max = "max"
    min = "min"
    center = "center"


class ProjectionMethodType(str, enum.Enum):
    integrate = "integrate"
    min = "min"
    max = "max"


CenteringType = Union[
    Tuple[CenteringTypeEnum, FieldName], CenteringTypeEnum, UnitfulCoordinate
]

uv = Union[ReturnsUnitfulValue, UnitfulValue]


class PlotDefinition(BaseModel):
    axes: Union[str, List[str]]
    center: CenteringType = "center"
    widths: Union[UnitfulValue, List[UnitfulValue]]
    min: Union[uv, List[uv], Dict[FieldName, uv]]
    max: Union[uv, List[uv], Dict[FieldName, uv]]
    source: Union[Projection, List[Projection]]


class ProjectionDefinition(PlotDefinition):
    fields_to_plot: Union[FieldName, List[FieldName]] = Field(None, alias="fields")
    weight_field: FieldName
    method: ProjectionMethodType = "integrate"
    data_source: DataSource = "all_data"


class ImageGallery(BaseModel):
    dataset: Union[str, List[str]]
    plots: List[PlotDefinition]
