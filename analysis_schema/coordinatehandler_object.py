from pydantic import BaseModel, Schema, create_model
from typing import Dict, List, Optional, Sequence, Set, Tuple, OrderedDict, Any
import enum

from .quantities import UnitfulCoordinate, Vector, Path, UnitfulValue, UnitfulArray
from .data_objects import DataObject
from .dataset import Dataset
from .products import Profile


class CoordinateHandler(BaseModel):
    # not sure what the input for data projection is, but it eventually becomes a dictionary
    data_projection: dict
    axis_id: dict
    y_axis: dict
    image_axis_name: dict
    x_axis: dict
    data_transform: dict
    axis_order: list
    ds: Dataset = None
    axis_name: dict
    name: str = None


print(CoordinateHandler.schema_json(indent=2))
