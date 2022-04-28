from typing import List, Optional

from ._data_store import Output
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

    def _run(self):
        # for the top level model, we override this.
        # Nested objects will still be recursive!
        # output_list = []
        # because this inside the _run() function,
        # it is wiped clean everytime it is called
        attribute_data = self.Data
        # creating an output instance to store viz
        output = Output()

        if attribute_data is not None:
            # the data does not get added to the output list, because we can't call
            # .save() or .show() on it
            for data in attribute_data:
                data._run()

        attribute_plot = self.Plot
        if attribute_plot is not None:
            for data_class in attribute_plot:
                for attribute in dir(data_class):
                    if attribute.endswith("Plot"):
                        plotting_attribute = getattr(data_class, attribute)
                        if plotting_attribute is not None:
                            output.add_output(plotting_attribute._run())
                        output_flat = [
                            viz for out in output._output_list for viz in out
                        ]
            return output_flat


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
