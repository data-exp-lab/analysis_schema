from pydantic import BaseModel
import yt


class Output:
    def __init__(self):
        self._output_list = []

    def add_output(self, ytmodel_plotresult):
        self._output_list.append(ytmodel_plotresult)


class DatasetFixture:
    """
    A class to hold all references and instantiated datasets. Also has a method to instantiate the data if it isn't already.
    There is a dictionary for dataset references and instantiated datasets.
    """

    def __init__(self):
        self.all_data = {}
        self._instantiated_datasets = {}

    def add_to_alldata(self, fn, DatasetName):
        """
        A function to track all dataset. 
        Stores dataset name, or if no name is provided, adds a number as the name. 
        """
        self.fn = fn
        if DatasetName is not None:
            self.DatasetName = DatasetName
        else:
            self.DatasetName = len(self.all_data.values())
        self.all_data[DatasetName] = fn

    def _instantiate_data(
        self, DatasetName,
    ):
        """
        Instantiates a dataset and stores it in a separate dictionary.
        Returns an instantiated (loaded into memory) dataset. 
        """
        ds = yt.load(self.all_data[DatasetName])
        self._instantiated_datasets[DatasetName] = ds
        return ds


dataset_fixture = DatasetFixture()
