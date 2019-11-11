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
    profiles : List[Profile]

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

### Sam adding more stuff

class LineBuffer(BaseModel):
    data : Dict[Tuple[str, str], UnitfulArray] = {}
    start_point : Tuple[UnitfulValue, UnitfulValue, UnitfulValue] = None
    end_point : Tuple[UnitfulValue, UnitfulValue, UnitfulValue] = None
    npoints : int = 0
    label : str = None
    ds : Dataset = None
    # not sure if vector is correct here
    points : Vector

class LinePlotDictionary(BaseModel):
    known_dimensions : dict = None

class LinePlot(BaseModel):
    plot_valid : bool
    # calling previous function
    lines : LineBuffer
    x_unit : str = None
    plot_type : str = 'line_plot'

class FieldTransform(BaseModel):
    # Unsure of this one
    func : Any # a function call of some kind
    name : str = None

class PlotDictionary(BaseModel):
    data_source: DataObject = None

class PlotContainer(BaseModel):
    plot_valid : bool = False
    ylabel : str = None
    field_transform : dict = None
    minorticks : dict = None
    font_color : str = None
    font_properties : tuple = None
    data_valid : bool = False
    # could be a pair of floats if iterable
    figure_size : float = None
    # not sure what the difference is between ds, dataset, or data_source
    data_source : DataObject = None
    xlabel : str = None
    ds : Dataset
    # should be DatasetSeries?
    ts : Dataset
    plot_type : str = None

class ImagePlotContainer(BaseModel):
    # 'Any' is used when 'Plot Dictionary' is the value, I was unsure if we want to call it directly
     background_color : Any
     colorbar_label : Any
     colormaps : dict
     callbacks : list = None
     colorbar_valid : bool = False
     cbar_minorticks : dict
     plots : Any






