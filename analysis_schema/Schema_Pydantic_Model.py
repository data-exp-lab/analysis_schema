from enum import Enum
from pathlib import Path
from enum import Enum
from pydantic import BaseModel, Field, constr
from typing import Generic, List, Union, Dict, Optional
import pydantic
from pydantic.main import create_model
from uuid import UUID, uuid4
from dataclasses import dataclass

#from pydantic.types import ModelOrDc

# TO DO: 
# domain contexts - add class and add conditional logic. What classes, attributes, and methods should be subject to domain flexibility?
# start a spreadsheet / google doc to track this?
# ontologies? - add? pull from? 
# what are essential yt methods and attributes that need to be a part of each data class?
# - what of these attributes should the user not see (be set to private in pydantic)
# - What of these attributes should the user see/customize?
# - what of these atrributes are astro-specific? is there anything that is essential and astro-specific?

# for data ouptut - what in yt holds the data? What is data in yt? What should the schema refer to - create a mini-model to hold data output. Have user name that output, like a variable name? Have an id assigned to it?

# data ouput idea - turn data points into properties for re-use

# @dataclass
# class InputOutputMapping:
#     combo1: Dict[str, List[str]] = {'registration': ['selection', 'reduction', 'transformation']}

class Dataset(BaseModel):
    """ 
    The dataset model to load and that will be drawn from for other classes. Filename is the only required field. 
    """
    filename: str
    name: str = "Data for Science"
    comments: Optional[str] 
    grammar: str = "registration"

class Fields(BaseModel):
    field: str
    # unit - domain specific
    unit: str
    comments: Optional[str]
    grammar: str = "selection"

class AxisPlot(BaseModel):
    axis: str
    comments: Optional[str]

class Center(BaseModel):
    center: str
    comments: Optional[str]

class Widths(BaseModel):
    width: str
    comments: Optional[str]

class ColorMap(BaseModel):
    # list of pre-determined strings
    astro_map: str = "plasma"

class Scale(BaseModel):
    # list of pre-determined strings
    scale: str = "log"

class Average(BaseModel):
    average_field: Fields
    comments: Optional[str]
    grammar: str = "reduction"

class Sum(BaseModel):
    sum_field: Fields
    comments: Optional[str]
    grammar: str = "reduction"

class Operations(BaseModel):
    operation: Union[Sum, Average]

class _PlotAttributes(BaseModel):
    # necessary and private plotting functions for all plots
    PlottingWindow: str = "1.0"

class DataSource(BaseModel):
    dataset: Dataset
    data_selection: Union[Fields, Operations]

class SlicePlot(BaseModel):
    Data: DataSource
    AxisPlot: Optional[List[AxisPlot]]
    CenterPlot: Optional[Center]
    WidthPlot: Optional[List[Widths]]
    Comments: Optional[str]
    Annotation : bool = False
    # color map - domain specific
    ColorMap: str = None
    _PlotFunctions: _PlotAttributes


class ytModel(BaseModel):
    '''
    An example for a yt analysis schema using Pydantic
    '''
    Plot: List[SlicePlot]

    class Config:
        title = 'yt example'
        underscore_attrs_are_private = True

# file_path = Path("Data.json")
# print(file_path)

test = ytModel(Plot = [{"Data": {"dataset": {"filename": "data.txt"}, 
                    "data_selection": {"field": "density", "unit": "kpc"}}}])

print("Instance Example:")
print(test.json(indent=2))
print()
print("Schema Example:")
print(test.schema_json(indent=2))
print()


# yt_dynamic = create_model("Dynamic_yt_model", dataset=(str, "file.txt"), 
#     FieldList = (list, ["density", "temperature"]), axis=(str, "x"))

# print(yt_dynamic.schema_json(indent=2))


# # print(dir(pydantic))
# # print(help(pydantic))

with open("pydantic_schema_file.json", "w") as file:
    file.write(test.schema_json(indent=2))
