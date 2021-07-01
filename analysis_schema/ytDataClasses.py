from .BaseModelFunctions import ytBaseModel, ytParameter, ytDataObjectAbstract
from pydantic import Field, BaseModel
from typing import Optional, List, Union, Tuple, Any
from pathlib import Path
import numpy as np

class Dataset(ytBaseModel):
    """
    The dataset to load. Filen name must be a string.

    Required fields: Filename
    """
    fn: Path = Field(alias="FileName", description='Must be string containing the (path to the file and the) file name')
    name: str = "Data for Science"
    comments: Optional[str]
    _yt_operation: str = "load"

class FieldNames(ytParameter):
    """
    Specify a field name from the dataset
    """
    # can't seeem to alias 'field' - maybe because the pydantic name 'Field' is called to do the alias?
    field: str
    # unit - domain specific
    # getting an error with unit enabled
    _unit: Optional[str]
    comments: Optional[str]

    def _run(self):
        fieldname = super()._run()
        if ',' in fieldname:
            fieldtype, field = fieldname.split(',')
            return (fieldtype, field)

class Sphere(ytDataObjectAbstract):
    """A sphere of points defined by a *center* and a *radius*.

    Args:
        ytBaseModel ([type]): [description]
    """
    # found in the 'selection_data_containers.py'
    center: List[float] = Field(alias='Center')
    radius: Union[float, Tuple[float, str]] = Field(alias='Radius')
    data_source: Optional[Dataset] = Field(alias="DataSet")
    _yt_operation: str = "sphere"

class Region(ytBaseModel):
    center: List[float]
    left_edge: List[float]
    right_edge: List[float]
    _yt_operation: str = "region"

class Slice(ytBaseModel):
    axis: Union[int, str]
    coord: float
    _yt_operation: "slice"

class SlicePlot(ytBaseModel):
    ds: Dataset = Field(alias='Dataset')
    fields: FieldNames = Field(alias='FieldNames')
    axis: str = Field(alias='Axis')
    center: Optional[Union[str, List[float]]] = Field(alias='Center')
    width: Optional[Union[List[str], Tuple[int, str]]] = Field(alias='Width')
    data_source: Optional[Sphere]
    Comments: Optional[str]
    _yt_operation: str = "SlicePlot"


class ProjectionPlot(ytBaseModel):
    ds: Optional[Dataset] = Field(alias='Dataset')
    fields: FieldNames = Field(alias='FieldNames')
    axis: Union[str, int] = Field(alias='Axis')
    # domain stuff here. Can we simplify? Contains operations stuff too
    center: Optional[str] = Field(alias='Center')
    # more confusing design. Can we simplify? This contain field names, units, and widths
    width: Optional[Union[tuple, float]] = Field(alias='Width')
    axes_unit: Optional[str] = Field(alias='AxesUnit')
    weight_field: Optional[FieldNames] = Field(alias='WeightFieldName')
    max_level: Optional[int] = Field(alias='MaxLevel')
    # need to sort this design out
    # might need to be a seperate class since we need to limit the length
    origin: Optional[Union[str, List[str]]] = Field(alias='Origin')
    #right handed? what does this mean?
    right_handed: Optional[bool] = Field(alias='RightHanded')
    fontsize: Optional[int] = Field(alias='FontSize')
    # TODO: a dict for dervied fields - can imporve
    field_parameters: Optional[dict] = Field(alias='FieldParameters')
    # better name?
    method: Optional[str] = Field(alias='Method')
    data_source: Optional[Union[Sphere, Region]] = Field(alias="DataSource", description="Select a subset of the dataset to visualize from the overall dataset")
    Comments: Optional[str]
    _yt_operation: str = "ProjectionPlot"


class PhasePlot(ytBaseModel):
    data_source: Union[Dataset, Any] = Field(alias='Dataset')
    x_field: FieldNames = Field(alias='xField')
    y_field: FieldNames = Field(alias='yField')
    z_fields: Union[FieldNames, List[FieldNames]] = Field(alias='zField(s)')
    weight_field: Optional[FieldNames]= Field(alias='WegihtFieldName')
    x_bins: Optional[int] = Field(alias='xBins')
    y_bins: Optional[int] = Field(alias='yBins')
    # different names and explaintions for accumulation and fractional and shading
    accumulation: Optional[Union[bool, List[bool]]] = Field(alias='Accumulation')
    fractional: Optional[bool] = Field(alias='Fractional')
    figure_size: Optional[int] = Field(alias='FigureSize')
    fontsize: Optional[int] = Field(alias='FontSize')
    # different name? Maybe should be an enum?
    shading: Optional[str] = Field(alias='Shading')
    Comments: Optional[str]
    _yt_operation: str = "PhasePlot"

class NapariVolume(ytBaseModel):
    ds: Dataset = Field(alias='Dataset')
    field: FieldNames = Field(alias='Field')
    resolution: Optional[Tuple] = (100, 100, 100)
    left_edge: Optional[Tuple] = (0., 0., 0.)
    right_edge: Optional[Tuple] = (1., 1., 1.)
    length_units: Optional[str] = 'code_length'
    take_log: Optional[int] = 1

    def _run(self, napari=False):
        if napari:
            # this gets run by the napari plugin for a schema, just returns a 3d ndarray
            data = self._get_ndarray()
            return data
        else:
            return None


    def _get_ndarray(self):
        # first instantiate the dataset
        ds = self.ds._run()

        frb = ds.r[
              self.left_edge[0]:self.right_edge[0]:complex(0, self.resolution[0]),
              self.left_edge[1]:self.right_edge[1]:complex(0, self.resolution[1]),
              self.left_edge[2]:self.right_edge[2]:complex(0, self.resolution[2]),
              ]

        field = self.field._run()

        if self.take_log:
            return np.log10(frb[field])
        else:
            return frb[field]


class Visualizations(BaseModel):
    # use pydantic basemodel
    SlicePlot: Optional[SlicePlot]
    ProjectionPlot: Optional[ProjectionPlot]
    PhasePlot: Optional[PhasePlot]
    Napari: Optional[NapariVolume]
