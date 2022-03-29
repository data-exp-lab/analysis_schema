from pydantic import BaseModel
import yt

# this is the list that all visualization outputs are collected. Maybe this also needs a class? Or some other data structure?
_output_list = []


class DatasetFixture:
    """
    A class to hold all references and instantiated datasets. Also has a method to instantiate the data if it isn't already.
    There is a dictionary for dataset references and instantiated datasets.
    """

    def __init__(self):
        self.all_data = {}
        self._instantiated_datasets = {}
        self.all_fields = {}

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
        # adding the fieldlist to a List. How to handle fieldlists for multiiple datasets?
        self.all_fields[DatasetName] = ds.field_list
        return ds


dataset_fixture = DatasetFixture()

class FieldFixture(DatasetFixture):

    def __init__(self):
        # how to account for field type?
        print("do I need to do this step?")

    def add_fields(self):
        self.all_fields.append((self.field_type, self.field))
        print("field list:", self.add_fields)
        return self.all_fields

field_fixture = FieldFixture()

    
