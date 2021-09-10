import enum
from typing import Any, Dict, List, Optional, OrderedDict, Sequence, Set, Tuple

from pydantic import BaseModel, Schema, create_model

from .data_objects import DataObject
from .dataset import Dataset
from .products import Profile
from .quantities import Path, UnitfulArray, UnitfulCoordinate, UnitfulValue, Vector


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
