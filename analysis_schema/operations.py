import typing
from pydantic import BaseModel, Schema, create_model

class Average(BaseModel):
    average: typing.Union[str, typing.Tuple[str, str]]
    weight: typing.Tuple[str, str] = None
    axis: typing.Union[typing.Tuple[str, str], str]

class Sum(BaseModel):
    sum: typing.Union[str, typing.Tuple[str, str]]
    axis: typing.Union[typing.Tuple[str, str], str]

class Minimum(BaseModel):
    minimum: typing.Union[str, typing.Tuple[str, str]]
    field: typing.Tuple[str, str]
    axis: typing.Union[typing.Tuple[str, str], str]

class Maximum(BaseModel):
    maximum: typing.Union[str, typing.Tuple[str, str]]
    field: typing.Tuple[str, str]
    axis: typing.Union[typing.Tuple[str, str], str]

class Integrate(BaseModel):
    integrate: typing.Union[str, typing.Tuple[str, str]]
    field: typing.Tuple[str, str]
    axis: typing.Union[typing.Tuple[str, str], str]

class Operation(BaseModel):
    operation: typing.Union[Average, Sum, Minimum, Maximum, Integrate]
