from pydantic import BaseModel
import yt

# _instantiated_datasets = {}

class DatasetFixture():

    all_data = {}
    _instantiated_datasets = {}
    
    def __init__(self, fn, DatasetName):   
        self.fn = fn
        if DatasetName is not None:
            self.DatasetName = DatasetName
        else:
            self.DatasetName = len(DatasetFixture.all_data.values())
        DatasetFixture.all_data[DatasetName] = fn

    def _instantiate_data(self, DatasetName, all_data=all_data, _instantiated_datasets=_instantiated_datasets):
        ds = yt.load(all_data[DatasetName])
        print("Instaniateed data:", ds)
        _instantiated_datasets[DatasetName] = ds
        print(_instantiated_datasets)
        return ds
