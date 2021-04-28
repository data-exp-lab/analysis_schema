#%%

from enum import Enum
from pydantic import BaseModel, Field, constr
from typing import Generic, List, Union, Dict, Optional, Sequence, Tuple
import pydantic
from pydantic.main import create_model
from inspect import getfullargspec
import yt

class ytBaseModel(BaseModel):
    _arg_mapping: dict = {}  # mapping from internal yt name to schema name
    _yt_operation: Optional[str]

    def _run(self):
        # this method actually executes the yt code

        # first make sure yt is imported and then get our function handle. This assumes
        # that our class name exists in yt's top level api.
        import yt
        print(yt.__version__)
        print(self._yt_operation)

        funcname = getattr(self, "_yt_operation", type(self).__name__)
        func = getattr(yt, funcname)
        print(f"pulled func {func}")

        # now we get the arguments for the function:
        # func_spec.args, which lists the named arguments and keyword arguments.
        # ignoring vargs and kw-only args for now...
        # see https://docs.python.org/3/library/inspect.html#inspect.getfullargspec
        func_spec = getfullargspec(func)
        print("spec", func_spec)

        # the list that we'll use to eventually call our function
        the_args = []

        # the argument position number at which we have default values (a little hacky, should
        # be a better way to do this, and not sure how to scale it to include *args and **kwargs)
        n_args = len(func_spec.args)  # number of arguments
        print("number of args:", n_args)
        if func_spec.defaults is None:
            # no default args, make sure we never get there...
            named_kw_start_at = n_args + 1
        else:
            # the position at which named keyword args start
            named_kw_start_at = n_args - len(func_spec.defaults)
        print(f"keywords start at {named_kw_start_at}")

        # loop over the call signature arguments and pull out values from our pydantic class .
        # this is recursive! will call _run() if a given argument value is also a ytBaseModel.
        for arg_i, arg in enumerate(func_spec.args):
            # check if we've remapped the yt internal argument name for the schema
            if arg == 'self':
                continue
            if arg in self._arg_mapping:
                arg = self._arg_mapping[arg]

            # get the value for this argument. If it's not there, attempt to set default values
            # for arguments needed for yt but not exposed in our pydantic class
            print(arg)
            try:
                arg_value = getattr(self, arg)
            except AttributeError:
                if arg_i >= named_kw_start_at:
                    # we are in the named keyword arguments, grab the default
                    # the func_spec.defaults tuple 0 index is the first named
                    # argument, so need to offset the arg_i counter
                    default_index = arg_i - named_kw_start_at
                    arg_value = func_spec.defaults[default_index]
                else:
                    raise AttributeError

            # check if this argument is itself a ytBaseModel for which we need to run
            # this should make this a fully recursive function?
            # if hasattr(arg_value,'_run'):
            if isinstance(arg_value, ytBaseModel) or isinstance(arg_value, ytParameter):
                print(
                    f"{arg_value} is a {type(arg_value)}, calling {arg_value}._run() now...")
                arg_value = arg_value._run()

            the_args.append(arg_value)
        print(the_args)
        return func(*the_args)

class ytParameter(BaseModel):
    _skip_these = ['comments']

    def _run(self):
        p = [getattr(self, key) for key in self.schema()[
            'properties'].keys() if key not in self._skip_these]
        if len(p) > 1:
            print("some error", p)
            raise ValueError(
                "whoops. ytParameter instances can only have single values")
        return p[0]


class Dataset(ytBaseModel):
    """ 
    The dataset model to load and that will be drawn from for other classes. Filename is the only required field. 
    """
    filename: str
    name: str = "Data for Science"
    comments: Optional[str] 
    _grammar: str = "registration"
    _yt_operation: str = "load"
    _arg_mapping: dict = {'fn' : 'filename'}
    

class Fields(ytParameter):
    field: str
    # unit - domain specific
    # getting an error with unit enabled
    _unit: Optional[str]
    comments: Optional[str]
    _grammar: str = "selection"

# class AxisPlot(ytParameter):
#     axis: str
#     comments: Optional[str]

class Center(ytParameter):
    center: str
    comments: Optional[str]

class Widths(ytParameter):
    width: str
    comments: Optional[str]

# class ColorMap(BaseModel):
#     # list of pre-determined strings
#     astro_map: str = "plasma"

# class Scale(BaseModel):
#     # list of pre-determined strings
#     scale: str = "log"

# class Average(BaseModel):
#     average_field: Fields
#     comments: Optional[str]
#     _grammar: str = "reduction"

# class Sum(BaseModel):
#     sum_field: Fields
#     comments: Optional[str]
#     _grammar: str = "reduction"

# class Operations(BaseModel):
#     operation: Union[Sum, Average]

# class DataSource(BaseModel):
#     dataset: Dataset
#     data_selection: Union[Fields, Operations]

class SlicePlot(ytBaseModel):
    Dataset: Dataset
    Field: Fields
    Axis: str
    CenterPlot: Optional[Center]
    WidthPlot: Optional[List[Widths]]
    Comments: Optional[str]
    _yt_operation: str = "SlicePlot"
    _arg_mapping: dict = {'ds': 'Dataset', 'fields': 'Field',
                          'axis': 'Axis', 'center': 'CenterPlot', 'width': 'WidthPlot'}
    #Annotation : bool = False
    # color map - domain specific
    #ColorMap: str = None
    #_PlotFunctions: _PlotAttributes

class ProjectionPlot(ytBaseModel):
    Dataset: Dataset
    Field: Fields
    Axis: str
    CenterPlot: Center
    WidthPlot: Optional[List[Widths]]
    Comments: Optional[str]
    _yt_operation: str = "ProjectionPlot"
    _arg_mapping: dict = {'ds': 'Dataset', 'fields': 'Field',
                          'axis': 'Axis', 'center': 'CenterPlot', 'width': 'WidthPlot'}

class PhasePlot(ytBaseModel):
    Dataset: Dataset
    xField: Fields
    yField: Fields
    zField: Union[Fields, List[Fields]]
    Comments: Optional[str]
    _yt_operation: str = "PhasePlot"
    _arg_mapping: dict = {'data_source': 'Dataset', 'x_field': 'xField', 'y_field': 'yField', 'z_fields': 'zField'}

class ytModel(ytBaseModel):
    '''
    An example for a yt analysis schema using Pydantic
    '''
    Plot: List[Union[SlicePlot, ProjectionPlot]]

    class Config:
        title = 'yt example'
        underscore_attrs_are_private = True
    
    def _run(self):
        # for the top level model, we override this. Nested objects will still be recursive!
        att = getattr(self, "Plot")
        return [p._run() for p in att]

json_slice = {"Plot": [{"Dataset": {
    "filename": "IsolatedGalaxy/galaxy0030/galaxy0030"},
    "Field": {"field": "density"},
    "Axis": "x"}]}

json_projection = {"Plot": [{"Dataset": {
    "filename": "IsolatedGalaxy/galaxy0030/galaxy0030"},
    "Field": {"field": "velocity_magnitude"},
    "Axis": "x",
    "CenterPlot": {"center": "c"}}]}

json_phase = {"Plot": [{"Dataset": {
    "filename": "IsolatedGalaxy/galaxy0030/galaxy0030"},
    "xField": {"field": "density"},
    "yField": {"field" : "temperature"},
    "zField": {"field": "velocity_magnitude"}}]}

analysis_model = ytModel(Plot= [{"Dataset": {
    "filename": "IsolatedGalaxy/galaxy0030/galaxy0030"},
    "Field": {"field": "density"},
    "Axis": "x"},
    {"Dataset": {
    "filename": "IsolatedGalaxy/galaxy0030/galaxy0030"},
    "Field": {"field": "velocity_magnitude"},
    "Axis": "x",
    "CenterPlot": {"center": "c"}}])

print(analysis_model)

# print("Instance Example:")
# print(analysis_model.json(indent=2))
# print()
# print("Schema Example:")
# print(analysis_model.schema_json(indent=2))
# print()
result = analysis_model._run()
result[0].show()

# yt_dynamic = create_model("Dynamic_yt_model", dataset=(str, "file.txt"),
#     FieldList = (list, ["density", "temperature"]), axis=(str, "x"))

# print(yt_dynamic.schema_json(indent=2))

with open("pydantic_schema_file.json", "w") as file:
    file.write(analysis_model.schema_json(indent=2))
