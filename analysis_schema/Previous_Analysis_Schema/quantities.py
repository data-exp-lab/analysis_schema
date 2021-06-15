import typing
from pydantic import BaseModel, Schema


class _UnitfulValue(BaseModel):
    value: float
    # This is a simplification -- we are not allowing for the case of full
    # unyt unit registries, etc
    unit: str = "unitary"


UnitfulValue = typing.Union[_UnitfulValue, typing.Tuple[float, str]]


class UnitfulArray(BaseModel):
    values: typing.List[float]
    unit: str = "unitary"
    dimensionality: int = -1  # -1 for none specified
    shape: typing.Tuple[int] = ()


class _UnitfulCoordinate(BaseModel):
    values: typing.List[float] = Schema([0.5, 0.5, 0.5], minItems=3, maxItems=3)
    unit: str = "unitary"


UnitfulCoordinate = typing.Union[
    _UnitfulCoordinate, typing.Tuple[typing.List[float], str]
]

unyt_array_model = typing.Union[typing.List[UnitfulValue], UnitfulArray]


class Vector(BaseModel):
    start_point: UnitfulCoordinate
    end_point: UnitfulCoordinate


class Path(BaseModel):
    points: typing.List[UnitfulCoordinate]
