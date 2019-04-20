import typing
from pydantic import BaseModel

class UnitfulValue(BaseModel):
    value: float
    # This is a simplification -- we are not allowing for the case of full
    # unyt unit registries, etc
    unit: str = "unitary"

class UnitfulArray(BaseModel):
    values: typing.List[float]
    unit: str = "unitary"

unyt_array_model = typing.Union[typing.List[UnitfulValue],
                                UnitfulArray]
# Just 3D for now
class Coordinate(BaseModel):
    values: UnitfulArray

class Vector(BaseModel):
    start_point: Coordinate
    end_point: Coordinate

class Path(BaseModel):
    points: typing.List[Coordinate]
