from pathlib import Path
from typing import List, Optional, Tuple, Union

from pydantic import BaseModel, Field

from ._data_store import dataset_fixture
from .base_model import ytBaseModel, ytDataObjectAbstract, ytParameter


class Dataset(ytBaseModel):
    """
    The dataset to load. Filename (fn) must be a string.

    Required fields: Filename, DatasetName
    """

    DatasetName: Optional[str]
    fn: Path = Field(
        alias="FileName",
        description="A string containing the (path to the file and the) file name",
    )
    comments: Optional[str]
    instantiate: bool = True
    _yt_operation: str = "load"

    def _run(self):
        if self.DatasetName in [dataset_fixture._instantiated_datasets.keys()]:
            return dataset_fixture._instantiated_datasets[self.DatasetName]
        else:
            dataset_fixture.add_to_alldata(self.fn, self.DatasetName)
            if self.instantiate is True:
                ds = dataset_fixture._instantiate_data(self.DatasetName)
                return ds


class FieldNames(ytParameter):
    """
    Specify a field name and field type from the dataset
    """

    # can't seeem to alias 'field' - maybe because the pydantic name 'Field' is called
    # to do the alias?
    field: str
    field_type: str
    # unit - domain specific
    # getting an error with unit enabled
    _unit: Optional[str]
    comments: Optional[str]

    def _run(self):
        # add field fixture?
        return (self.field_type, self.field)


class Sphere(ytDataObjectAbstract):
    """A sphere of points defined by a *center* and a *radius*.
    """

    # found in the 'selection_data_containers.py'
    center: List[float] = Field(alias="Center")
    radius: Union[float, Tuple[float, str]] = Field(alias="Radius")
    data_source: Optional[Dataset] = Field(alias="DataSet")
    _yt_operation: str = "sphere"


class Region(ytDataObjectAbstract):
    """A cartesian box data selection object
    """

    center: List[float]
    left_edge: List[float]
    right_edge: List[float]
    _yt_operation: str = "region"


class Slice(ytDataObjectAbstract):
    """An axis-aligned 2-d slice data selection object"""

    axis: Union[int, str]
    coord: float
    _yt_operation: str = "slice"


class DataSource3D(ytBaseModel):
    """Select a subset of the dataset to visualize from the overall dataset"""

    sphere: Optional[Sphere]
    region: Optional[Region]

    def _run(self):
        for container in [self.sphere, self.region]:
            if container:
                return container._run()


class SlicePlot(ytBaseModel):
    """Axis-aligned slice plot."""

    ds: Optional[List[Dataset]] = Field(alias="Dataset")
    fields: FieldNames = Field(alias="FieldNames")
    normal: str = Field(alias="Axis")
    center: Optional[Union[str, List[float]]] = Field(alias="Center")
    width: Optional[Union[List[str], Tuple[int, str]]] = Field(alias="Width")
    data_source: Optional[DataSource3D] = Field(alias="DataSource")
    Comments: Optional[str]
    _yt_operation: str = "SlicePlot"
    _known_kwargs: Optional[List[str]] = [
        "data_source",
    ]

    def _run(self):
        """
        This _run function checks if this plot has a value for the `ds` arguement (or attribute). 
        If it does not, then it looks for data in the `DatasetFixture` class. 
        If there is more than one instantiated dataset, a plot will be created for each dataset.

        return: a dataset, or a list of datasets
        """
        super_list = []
        if self.ds is None:
            for instantiated_keys in list(
                dataset_fixture._instantiated_datasets.keys()
            ):
                self.ds = dataset_fixture._instantiated_datasets[instantiated_keys]
                # append output to a list to return
                super_list.append(super()._run())
                # put each 'self' into the output
                # when calling `._run()` there is no plotting attribute, so it is not added to the output list
            return super_list
        if self.ds is not None:
            if isinstance(self.ds, list):
                for data in self.ds:
                    self.ds = data
                    super_list.append(super()._run())
                return super_list
            super_list.append(super()._run())
            return super_list


class ProjectionPlot(ytBaseModel):
    """Axis-aligned projection plot."""

    ds: Optional[List[Dataset]] = Field(alias="Dataset")
    fields: FieldNames = Field(alias="FieldNames")
    normal: Union[str, int] = Field(alias="Axis")
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
    data_source: Optional[DataSource3D] = Field(alias="DataSource")
    Comments: Optional[str]
    _yt_operation: str = "ProjectionPlot"

    def _run(self):
        """
        This _run function checks if this plot has a value for the `ds` arguement (or attribute). 
        If it does not, then it looks for data in the `DatasetFixture` class. 
        If there is more than one instantiated dataset, a plot will be created for each dataset.

        return: a dataset, or a list of datasets
        """
        super_list = []
        if self.ds is None:
            for instantiated_keys in list(
                dataset_fixture._instantiated_datasets.keys()
            ):
                self.ds = dataset_fixture._instantiated_datasets[instantiated_keys]
                # append output to a list to return
                super_list.append(super()._run())
                # put each 'self' into the output
                # when calling `._run()` there is no plotting attribute, so it is not added to the output list
            return super_list
        if self.ds is not None:
            if isinstance(self.ds, list):
                for data in self.ds:
                    self.ds = data
                    super_list.append(super()._run())
                return super_list
            super_list.append(super()._run())
            return super_list

    @property
    def axis(self):
        # yt <= 4.1.0 uses axis instead of normal, this aliasing allows the
        # recursive function to pull the right attribute.
        return self.normal


class PhasePlot(ytBaseModel):
    """A yt phase plot"""

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

    def _run(self):
        super_list = []
        if self.ds is None:
            # self.ds = list(DatasetFixture._instantiated_datasets.values())[0]
            for instantiated_keys in list(
                dataset_fixture._instantiated_datasets.keys()
            ):
                self.ds = dataset_fixture._instantiated_datasets[instantiated_keys]
                super_list.append(super()._run())
                # put each 'self' into the output
                # when calling `._run()` there is no plotting attribute, so it is not added to the output list
        return super_list
        # return super()._run()


class Visualizations(BaseModel):
    """
    This class organizes the attributes below so users can select the plot by name,
    and see the correct arguments as suggestions
    """

    # use pydantic basemodel
    SlicePlot: Optional[SlicePlot]
    ProjectionPlot: Optional[ProjectionPlot]
    PhasePlot: Optional[PhasePlot]
