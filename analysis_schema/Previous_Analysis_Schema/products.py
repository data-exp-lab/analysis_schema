from pydantic import BaseModel

from .data_objects import DataObject
from .dataset import Dataset
from .operations import Operation


class Projection(BaseModel):
    source: DataObject = {"all_data": {}}
    operation: Operation = {"sum": "density", "axis": "x"}


class ProfileND(BaseModel):
    data_source: DataObject
    ds = Dataset


class Profile(BaseModel):
    pass
