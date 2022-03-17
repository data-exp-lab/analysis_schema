from pydantic import BaseModel
import yt

# this is the list that all visualization outputs are collected. Maybe this also needs a class? Or some other data structure?
_output_list = []


class DatasetFixture:
    """
    A class to hold all references and instantiated datasets. Also has a method to instantiate the data if it isn't already.
    There is a dictionary for dataset references and instantiated datasets.
    """

    all_data = {}
    _instantiated_datasets = {}

    def __init__(self, fn, DatasetName):
        self.fn = fn
        if DatasetName is not None:
            self.DatasetName = DatasetName
        else:
            self.DatasetName = len(DatasetFixture.all_data.values())
        DatasetFixture.all_data[DatasetName] = fn

    def _instantiate_data(
        self,
        DatasetName,
        all_data=all_data,
        _instantiated_datasets=_instantiated_datasets,
    ):
        ds = yt.load(all_data[DatasetName])
        _instantiated_datasets[DatasetName] = ds
        return ds
