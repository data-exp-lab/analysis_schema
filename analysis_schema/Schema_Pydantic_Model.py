
from pydantic import BaseModel, Field, constr
from typing import Generic, List, Union, Dict, Optional, Sequence, Tuple
import pydantic
from pydantic.main import create_model
from inspect import getfullargspec


class ytBaseModel(BaseModel):
    _arg_mapping: dict = {}  # mapping from internal yt name to schema name
    _yt_operation: Optional[str]

    def _run(self):
        # this method actually executes the yt code


        # first make sure yt is imported and then get our function handle. This assumes
        # that our class name exists in yt's top level api.
        # will only work with yt 4.0. Version 3.6.1 does not grap the arguements
        import yt
        #print(yt.__version__)
        print(self._yt_operation)
    
        funcname = getattr(self, "_yt_operation", type(self).__name__)
        func = getattr(yt, funcname)
        #print(f"pulled func {func}")

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
    """
    The fields dataclasses allows uers to type in a string for a field in the dataset. Field is the only required attribute. 
    """
    field: str
    # unit - domain specific
    # getting an error with unit enabled
    _unit: Optional[str]
    comments: Optional[str]

class SlicePlot(ytBaseModel):
    """
    The slice plot data class maps to a yt operation and parameters. Dataset, Field and Axis are required. All other attributes will take the yt default if not specified. 
    """
    Dataset: Dataset
    Field: Fields
    Axis: str
    CenterPlot: Optional[str]
    WidthPlot: Optional[List[str]]
    Comments: Optional[str]
    _yt_operation: str = "SlicePlot"
    _arg_mapping: dict = {'ds': 'Dataset', 'fields': 'Field',
                          'axis': 'Axis', 'center': 'CenterPlot', 'width': 'WidthPlot'}
  

class ProjectionPlot(ytBaseModel):
    """
   The projection plot data class maps to a yt operation and parameters. Dataset, Field, Axis and AxisUnit are required. All other attributes will take the yt default if not specified.
    """
    Dataset: Dataset
    Field: Fields
    Axis: Union[str, int]
    # domain stuff here. Can we simplify? Contains operations stuff too
    CenterPlot: Optional[str]
    # more confusing design. Can we simplify? This contain field names, units, and widths
    WidthPlot: Optional[Union[tuple, float]]
    WeightedField: Optional[Fields]
    AxesUnit: str
    # need to sort this design out
    # might need to be a seperate class since we need to limit the length
    Origin: Optional[Union[str, Sequence]]
    Comments: Optional[str]
    _yt_operation: str = "ProjectionPlot"
    _arg_mapping: dict = {'ds': 'Dataset', 'fields': 'Field',
                            'axis': 'Axis', 'center': 'CenterPlot',
                          'weight_field': 'WeightedField', 'axes_unit': 'AxesUnit'}

class PhasePlot(ytBaseModel):
    """
    The phase plot data class maps to a yt operation and parameters. 
    """
    Dataset: Dataset
    xField: Fields
    yField: Fields
    zField: Union[Fields, List[Fields]]
    WeightedField: Optional[Fields]
    xBins: Optional[int]
    yBins: Optional[int]
    # different names and explaintions for accumulation and fractional and shading
    Accumulation: Optional[Union[bool, List[bool]]]
    Fractional: Optional[bool]
    FigureSize: Optional[int]
    FontSize: Optional[int]
    # different name? Maybe should be an enum?
    Shading: Optional[str]
    Comments: Optional[str]
    _yt_operation: str = "PhasePlot"
    _arg_mapping: dict = {'data_source': 'Dataset', 'x_field': 'xField', 'y_field': 'yField', 'z_fields': 'zField', 'weight_field': 'WeightedField', 'x_bins': 'xBins', 'y_bins': 'yBins', 'accumulation': 'Accumulation', 'fractional': 'Fractional', 'figure_size': 'FigureSize', 'fontsize': 'FontSize',
    'shading': 'Shading'}

# outer most model
class ytModel(ytBaseModel):
    '''
    An example for a yt analysis schema using Pydantic
    '''
    Plot: List[Union[PhasePlot, SlicePlot, ProjectionPlot]]

    class Config:
        title = 'yt example'
        underscore_attrs_are_private = True
    
    def _run(self):
        # for the top level model, we override this. Nested objects will still be recursive!
        att = getattr(self, "Plot")
        # print("this is the att:", att[0])
        # for p in att:
        #     print("this is p:", p._yt_operation)
        return [p._run() for p in att]

# json for a slice plot
json_slice = {"Dataset": {
    "filename": "IsolatedGalaxy/galaxy0030/galaxy0030"},
    "Field": {"field": "density"},
    "Axis": "x"}

# json for a projeciton plot
json_projection = {"Dataset": {
    "filename": "IsolatedGalaxy/galaxy0030/galaxy0030"},
    "Field": {"field": "density"},
    "Axis": "y", 
    "CenterPlot": "c",
    "WeightedField": {"field": "velocity_magnitude"},
    "AxesUnit": "cm"}

# json for a phase plot
json_phase = {"Dataset": {
    "filename": "IsolatedGalaxy/galaxy0030/galaxy0030"},
    "xField": {"field": "density"},
    "yField": {"field" : "temperature"},
    "zField": {"field": "velocity_magnitude"},
    "WeightedField": {"field": "density"},
    "xBins": 100,
    "yBins": 100,
    "Accumulation": False,
    "Fractional": True,
    "FigureSize": 8,
    "FontSize": 16,
    "Shading": "nearest"}

# create yt model and print
analysis_model = ytModel(Plot= [json_phase, json_slice, json_projection])
print(analysis_model)

# show plot results
result = analysis_model._run()
result[0].show()
result[1].show()
result[2].show()

# write schema out to a file
with open("pydantic_schema_file.json", "w") as file:
    file.write(analysis_model.schema_json(indent=2))


