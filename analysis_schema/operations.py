import typing
from pydantic import BaseModel

class Average(BaseModel):
    field: typing.Tuple[str, str]
    weight: typing.Tuple[str, str] = None
    axis: typing.Union[typing.Tuple[str, str], str]

class Sum(BaseModel):
    field: typing.Tuple[str, str]
    axis: typing.Union[typing.Tuple[str, str], str]

class Minimum(BaseModel):
    field: typing.Tuple[str, str]
    axis: typing.Union[typing.Tuple[str, str], str]

class Maximum(BaseModel):
    field: typing.Tuple[str, str]
    axis: typing.Union[typing.Tuple[str, str], str]

class Integrate(BaseModel):
    field: typing.Tuple[str, str]
    axis: typing.Union[typing.Tuple[str, str], str]

operations = typing.Union[Average, Sum, Minimum, Maximum, Integrate]
