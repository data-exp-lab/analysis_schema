import typing
from pydantic import BaseModel
from .operations import operations
from .data_objects import data_objects

class Projection(BaseModel):
    source: data_objects
    operation: operations
