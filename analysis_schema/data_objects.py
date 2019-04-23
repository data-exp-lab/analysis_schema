import typing
from pydantic import BaseModel
from .quantities import Coordinate, Vector, Path, UnitfulValue, UnitfulArray

class Sphere(BaseModel):
    center: Coordinate
    radius: UnitfulValue

class Region(BaseModel):
    left_edge: Coordinate
    right_edge: Coordinate

class AllData(BaseModel):
    pass

data_objects = typing.Union[Region, Sphere, AllData]

class DataSource(BaseModel):
    source: typing.Union[data_objects, typing.List[data_objects]]
