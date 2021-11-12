from pathlib import Path
from typing import List, Optional, Tuple, Union

from pydantic import BaseModel, Field

from .base_model_functions import ytBaseModel, ytDataObjectAbstract, ytParameter


class Dataset(ytBaseModel):
    """
    The dataset to load. Filen name must be a string.

    Required fields: Filename
    """

    fn: Path = Field(
        alias="FileName",
        description="A string containing the (path to the file and the) file name",
    )
    DatasetName: Optional[str]
    comments: Optional[str]
    _yt_operation: str = "load"


class FieldNames(ytParameter):
    """
    Specify a field name from the dataset
    """

    # can't seeem to alias 'field' - maybe because the pydantic name 'Field' is called
    # to do the alias?
    field: str
    # unit - domain specific
    # getting an error with unit enabled
    _unit: Optional[str]
    comments: Optional[str]


class Sphere(ytDataObjectAbstract):
    """A sphere of points defined by a *center* and a *radius*.

    Args:
        ytBaseModel ([type]): [description]
    """

    # found in the 'selection_data_containers.py'
    center: List[float] = Field(alias="Center")
    radius: Union[float, Tuple[float, str]] = Field(alias="Radius")
    data_source: Optional[Dataset] = Field(alias="DataSet")
    _yt_operation: str = "sphere"


class Region(ytDataObjectAbstract):
    """summary

    Args:
        ytDataObjectAbstract ([type]): [description]
    """

    center: List[float]
    left_edge: List[float]
    right_edge: List[float]
    _yt_operation: str = "region"


class Slice(ytDataObjectAbstract):
    axis: Union[int, str]
    coord: float
    _yt_operation: "slice"


class SlicePlot(ytBaseModel):
    ds: Optional[Dataset] = Field(alias="Dataset")
    fields: FieldNames = Field(alias="FieldNames")
    axis: str = Field(alias="Axis")
    center: Optional[Union[str, List[float]]] = Field(alias="Center")
    width: Optional[Union[List[str], Tuple[int, str]]] = Field(alias="Width")
    data_source: Optional[Sphere]
    Comments: Optional[str]
    _yt_operation: str = "SlicePlot"


class ProjectionPlot(ytBaseModel):
    ds: Optional[Dataset] = Field(alias="Dataset")
    fields: FieldNames = Field(alias="FieldNames")
    axis: Union[str, int] = Field(alias="Axis")
    # domain stuff here. Can we simplify? Contains operations stuff too
    center: Optional[str] = Field(alias="Center")
    # more confusing design. Can we simplify? This contain field names, units, and
    # widths
    width: Optional[Union[tuple, float]] = Field(alias="Width")
    axes_unit: Optional[str] = Field(alias="AxesUnit")
    weight_field: Optional[FieldNames] = Field(alias="WeightFieldName")
    max_level: Optional[int] = Field(alias="MaxLevel")
    # need to sort this design out
    # might need to be a seperate class since we need to limit the length
    origin: Optional[Union[str, List[str]]] = Field(alias="Origin")
    # right handed? what does this mean?
    right_handed: Optional[bool] = Field(alias="RightHanded")
    fontsize: Optional[int] = Field(alias="FontSize")
    # TODO: a dict for dervied fields - can imporve
    field_parameters: Optional[dict] = Field(alias="FieldParameters")
    # better name?
    method: Optional[str] = Field(alias="Method")
    msg = "Select a subset of the dataset to visualize from the overall dataset"
    data_source: Optional[Union[Sphere, Region]] = Field(
        alias="DataSource", description=msg,  # skip: isort
    )
    Comments: Optional[str]
    _yt_operation: str = "ProjectionPlot"


class PhasePlot(ytBaseModel):
    data_source: Optional[Dataset] = Field(alias="Dataset")
    x_field: FieldNames = Field(alias="xField")
    y_field: FieldNames = Field(alias="yField")
    z_fields: Union[FieldNames, List[FieldNames]] = Field(alias="zField(s)")
    weight_field: Optional[FieldNames] = Field(alias="WegihtFieldName")
    x_bins: Optional[int] = Field(alias="xBins")
    y_bins: Optional[int] = Field(alias="yBins")
    # different names and explaintions for accumulation and fractional and shading
    accumulation: Optional[Union[bool, List[bool]]] = Field(alias="Accumulation")
    fractional: Optional[bool] = Field(alias="Fractional")
    figure_size: Optional[int] = Field(alias="FigureSize")
    fontsize: Optional[int] = Field(alias="FontSize")
    # different name? Maybe should be an enum?
    shading: Optional[str] = Field(alias="Shading")
    Comments: Optional[str]
    _yt_operation: str = "PhasePlot"


class Visualizations(BaseModel):
    """
    This class organizes the attributes below so users can select the plot by name,
    and see the correct arguments as suggestiongs

    Args:
        BaseModel (Pydantic BaseModel): [description]
    """

    # use pydantic basemodel
    SlicePlot: Optional[SlicePlot]
    ProjectionPlot: Optional[ProjectionPlot]
    PhasePlot: Optional[PhasePlot]
