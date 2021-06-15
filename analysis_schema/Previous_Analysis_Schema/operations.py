import typing
from pydantic import BaseModel, Schema, create_model


class Average(BaseModel):
    average: typing.Union[str, typing.Tuple[str, str]]
    weight: typing.Tuple[str, str] = None
    axis: typing.Union[None, typing.Tuple[str, str], str]


ReturnsUnitfulValue = typing.Union[Average]


class Sum(BaseModel):
    sum: typing.Union[str, typing.Tuple[str, str]]
    axis: typing.Union[None, typing.Tuple[str, str], str] = None


ReturnsUnitfulValue = typing.Union[ReturnsUnitfulValue, Sum]


class Minimum(BaseModel):
    minimum: typing.Union[str, typing.Tuple[str, str]]
    axis: typing.Union[None, typing.Tuple[str, str], str] = None


ReturnsUnitfulValue = typing.Union[ReturnsUnitfulValue, Minimum]


class Maximum(BaseModel):
    maximum: typing.Union[str, typing.Tuple[str, str]]
    axis: typing.Union[None, typing.Tuple[str, str], str] = None


ReturnsUnitfulValue = typing.Union[ReturnsUnitfulValue, Maximum]


class ArgMin(BaseModel):  # location of the maximum value
    arg_min: typing.Tuple[str, str]


ReturnsUnitfulCoordinate = typing.Union[ArgMin]


class ArgMax(BaseModel):  # location of the maximum value
    arg_max: typing.Tuple[str, str]


ReturnsUnitfulCoordinate = typing.Union[ReturnsUnitfulCoordinate, ArgMin]


class Integrate(BaseModel):
    integrate: typing.Union[str, typing.Tuple[str, str]]
    field: typing.Tuple[str, str]
    axis: typing.Union[typing.Tuple[str, str], str]


class Operation(BaseModel):
    operation: typing.Union[Average, Sum, Minimum, Maximum, Integrate]
