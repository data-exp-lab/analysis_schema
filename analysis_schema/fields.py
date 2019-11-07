import typing
import enum
from pydantic import BaseModel, Schema, create_model

class SamplingTypeEnum(str, enum.Enum):
    cell = "cell"
    discrete = "discrete"

class FieldParameter(BaseModel):
    pass

class SpatialValidator(BaseModel):
    ghost_zones: int = 0

class ParameterValidator(BaseModel):
    parameters: typing.List[str] = []

class PropertyValidator(BaseModel):
    property_name: str

FieldValidator = typing.Union[SpatialValidator, ParameterValidator,
                              PropertyValidator]

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
    nodal_flag: typing.Tuple[int, int, int] = (0,0,0)
