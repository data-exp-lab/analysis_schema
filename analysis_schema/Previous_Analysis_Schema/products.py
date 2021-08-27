import typing
from pydantic import BaseModel, Schema
from .operations import Operation, Sum
from .data_objects import AllData, DataObject
from .dataset import Dataset


class Projection(BaseModel):
    source: DataObject = {"all_data": {}}
    operation: Operation = {"sum": "density", "axis": "x"}


class ProfileND(BaseModel):
    data_source: DataObject
    ds = Dataset


class Profile(BaseModel):
    pass
