import contextlib
from pathlib import PosixPath

import yt


class Output:
    def __init__(self):
        self._output_list = []

    def add_output(self, ytmodel_plotresult):
        self._output_list.append(ytmodel_plotresult)


class DatasetContext:
    def __init__(self, fn, *args, **kwargs):
        self.filename = fn
        self.load_args = args
        self.load_kwargs = kwargs

    @contextlib.contextmanager
    def load(self):
        ds = yt.load(self.filename, *self.load_args, **self.load_kwargs)
        try:
            yield ds
        finally:
            # ds.close doesnt do anything for majority of frontends... might
            # as well call it though.
            ds.close()

    @contextlib.contextmanager
    def load_sample(self):
        ds = yt.load_sample(self.filename, *self.load_args, **self.load_kwargs)
        try:
            yield ds
        finally:
            # ds.close doesnt do anything for majority of frontends... might
            # as well call it though.
            ds.close()


class DataStore:
    """
    A class to hold all dataset references.
    """

    def __init__(self):
        self.available_datasets = {}

    def store(self, fn: str, dataset_name: str = None):
        """
        A function to track all dataset.
        Stores dataset name, or if no name is provided,
        adds a number as the name.
        """
        dataset_name = self.validate_name(fn, dataset_name)

        if dataset_name not in self.available_datasets:
            self.available_datasets[dataset_name] = DatasetContext(fn)

    def validate_name(self, fn: str, dataset_name: str = None):
        if dataset_name is None:
            if isinstance(fn, PosixPath):
                fn = str(fn)
            dataset_name = fn
        return dataset_name

    def retrieve(
        self,
        dataset_name: str,
    ):
        """
        Instantiates a dataset and stores it in a separate dictionary.
        Returns a dataset context
        """
        if dataset_name in self.available_datasets:
            return self.available_datasets[dataset_name]
        else:
            raise KeyError(f"{dataset_name} is not in the DataStore")

    def list_available(self):
        return list(self.available_datasets.keys())
