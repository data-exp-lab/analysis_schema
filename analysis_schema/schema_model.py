from typing import List, Optional

from .base_model import ytBaseModel
from .data_classes import Dataset, Visualizations


class ytModel(ytBaseModel):
    """
    Create a model in the form of a json schema, using the yt data classes. As values
    are added to the file referencing the schema, the function `run` with be called
    recursively to acccess nested yt elements and run the yt code.

    The run function iterates through the attributes of the class and runs this values
    entered for those attributes and puts the output into a list. This list will be
    iterated through to render and display the output.
    """

    Data: Optional[List[Dataset]]
    Plot: Optional[List[Visualizations]]

    class Config:
        title = "yt Schema Model for Descriptive Visualization and Analysis"
        underscore_attrs_are_private = True


schema = ytModel
schema_dict = schema.schema()

# create a dict to store the arguments required to instantiate an empty model
# useful for generating schemas from subsets of a model (see cli.py for an example)
_empty_model_registry = {}
_empty_model_registry["ytModel"] = (
    ytModel,
    dict(Data=[{"FileName": "", "DatasetName": ""}], Plot=[{}]),
)
_model_types = list(_empty_model_registry.keys())
