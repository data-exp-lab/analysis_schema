import enum
from typing import List, Tuple, Union, Dict
from pydantic import BaseModel, Schema, create_model, Field
from .quantities import UnitfulValue, UnitfulCoordinate
from .fields import FieldName
from .operations import ReturnsUnitfulValue


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
    fields_to_plot: Union[FieldName, List[FieldName]] = Field(None, alias="fields")
    axes: Union[str, List[str]]
    center: CenteringType = "center"
    widths: Union[UnitfulValue, List[UnitfulValue]]
    min: Union[uv, List[uv], Dict[FieldName, uv]]
    max: Union[uv, List[uv], Dict[FieldName, uv]]


class ProjectionDefinition(PlotDefinition):
    weight_field: FieldName
    method: ProjectionMethodType = "integrate"


class ImageGallery(BaseModel):
    dataset: Union[str, List[str]]
    projections: List[ProjectionDefinition]
