from pydantic import BaseModel, Schema, create_model
from typing import Dict, List, Optional, Sequence, Set, Tuple, OrderedDict, Any
import enum

from .quantities import UnitfulCoordinate, Vector, Path, UnitfulValue, UnitfulArray
from .data_objects import DataObject
from .dataset import Dataset
from .products import Profile


class CoordinateHandler(BaseModel):
    # not sure what the input for data projection is, but it eventually becomes a dictionary
    data_projection: Dict
    axis_id: Dict
    y_axis: Dict
    image_axis_name: Dict
    x_axis: Dict
    data_transform: Dict
    axis_order: List
    ds: Dataset = None
    axis_name: Dict
    name: str = None
