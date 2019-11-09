import typing
import enum
from pydantic import BaseModel, Schema, create_model
from . import quantities

_parameter_value_types = typing.Union[
    quantities.UnitfulArray,
    quantities.UnitfulValue,
    quantities.UnitfulArray,
    quantities.UnitfulCoordinate,
    quantities.Vector,
    quantities.Path,
]


class SamplingTypeEnum(str, enum.Enum):
    cell = "cell"
    discrete = "discrete"


class FieldParameter(BaseModel):
    name: str = None
    value: _parameter_value_types = None


class SpatialValidator(BaseModel):
    ghost_zones: int = 0


class ParameterValidator(BaseModel):
    parameters: typing.List[FieldParameter] = []


class PropertyValidator(BaseModel):
    property_name: str


FieldValidator = typing.Union[SpatialValidator, ParameterValidator, PropertyValidator]


class FieldDefinition(BaseModel):
    validators: typing.List[FieldValidator] = []
    sampling_type: SamplingTypeEnum = SamplingTypeEnum.cell
    name: str
    units: str
    dimensions: str
    take_log: bool
    display_field: bool
    vector_field: bool
    prescription: str
    nodal_flag: typing.Tuple[int, int, int] = (0, 0, 0)
