import typing
from pydantic import BaseModel
from .quantities import Coordinate, Vector, Path, UnitfulValue, UnitfulArray

class Sphere(BaseModel):
    center: Coordinate
    radius: UnitfulValue

class Region(BaseModel):
    left_edge: Coordinate
    right_edge: Coordinate

data_objects = typing.Union[Region, Sphere]

class DataSource(BaseModel):
    source: typing.Union[data_objects, typing.List[data_objects]]
