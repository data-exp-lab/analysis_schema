import typing

from pydantic import BaseModel, Schema

from .data_objects import AllData, DataObject
from .dataset import Dataset
from .operations import Operation, Sum


class Projection(BaseModel):
    source: DataObject = {"all_data": {}}
    operation: Operation = {"sum": "density", "axis": "x"}


class ProfileND(BaseModel):
    data_source: DataObject
    ds = Dataset


class Profile(BaseModel):
    pass
