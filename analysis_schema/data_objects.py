import typing
import enum
from pydantic import BaseModel, Schema, create_model
from .quantities import UnitfulCoordinate, Vector, Path, UnitfulValue, UnitfulArray


class Sphere(BaseModel):
    center: UnitfulCoordinate
    radius: UnitfulValue


class SphereID(BaseModel):
    sphere: Sphere


class Region(BaseModel):
    left_edge: UnitfulCoordinate
    right_edge: UnitfulCoordinate


class RegionID(BaseModel):
    region: Region


class AllData(BaseModel):
    pass


class AllDataID(BaseModel):
    all_data: typing.Union[AllData, None]


DataObject = DataSource = typing.Union[AllDataID, RegionID, SphereID]
