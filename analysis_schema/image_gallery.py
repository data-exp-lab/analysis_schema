import enum
from typing import List, Tuple, Union
from pydantic.fields import Field
from pydantic import BaseModel, Schema, create_model
from .quantities import UnitfulValue, UnitfulCoordinate
from .fields import FieldName


class CenteringTypeEnum(str, enum.Enum):
    max = "max"
    min = "min"
    center = "center"


CenteringType = Union[
    Tuple[CenteringTypeEnum, FieldName], CenteringTypeEnum, UnitfulCoordinate
]


class ProjectionDefinition(BaseModel):
    fields_to_plot: Union[FieldName, List[FieldName]] = Field(None, alias="fields")
    weight_field: FieldName
    axes: Union[str, List[str]]
    center: CenteringType = "center"
    widths: Union[UnitfulValue, List[UnitfulValue]]


class ImageGallery(BaseModel):
    dataset: Union[str, List[str]]
    projections: List[ProjectionDefinition]
