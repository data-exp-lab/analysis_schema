from pydantic import BaseModel, Schema, create_model
from typing import Dict, List, Optional, Sequence, Set, Tuple, OrderedDict, Any
import enum

from .quantities import UnitfulCoordinate, Vector, Path, UnitfulValue, UnitfulArray
from .data_objects import DataObject
from .dataset import Dataset
from .products import Profile

class FixedResolutionBuffer(BaseModel):
    period: Tuple[UnitfulValue, UnitfulValue] = None
    data : Dict[Tuple[str, str], UnitfulArray] = {}
    antialias : bool = True
    periodic : bool = False
    bounds : List[UnitfulValue]
    buff_size : Tuple[int, int]
    filters : list = []
    axis : int = 0
    data_source: DataObject = None
    # wasn't sure what to put for ds from the custom types in qunatities
    ds: Dataset = None

class ProfilePlot(BaseModel):
    # two x_logs?
    x_log : bool = None
    y_log : bool = None
    x_title : str = None
    y_title : str = None
    profiles : list[Profile]

class PhasePlot(BaseModel):
    x_log : bool = None
    y_log : bool = None
    plot_title : str = None
    plot_type : str = 'Phase'
    xlim : Tuple[UnitfulValue, UnitfulValue] = None
    ylim : Tuple[UnitfulValue, UnitfulValue] = None

class PhasePlotMPL(BaseModel):
    figure_size : Tuple[int, int]
    draw_colorbar : bool = True
    ax_text_size : List[float]
    image : Any
    cb_size : float
    aspect : float = 1.0
    draw_axes : bool = True
    initfinished : bool = False
    top_buff_size : float
    # this attribute eventually holds a color, does that get encoded into the typing/
    cb : tuple = None

