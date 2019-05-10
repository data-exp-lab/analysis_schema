import typing
from pydantic import BaseModel, Schema
from .operations import Operation, Sum
from .data_objects import AllData, DataObject

class Projection(BaseModel):
    source: DataObject = {"all_data": {}}
    operation: Operation = {"sum": "density", "axis": "x"}
