import contextlib
from pathlib import PosixPath
from typing import Optional

import yt


class Output:
    def __init__(self):
        self._output_list = []

    def add_output(self, ytmodel_plotresult):
        self._output_list.append(ytmodel_plotresult)


class DatasetContext:
    def __init__(self, fn, *args, in_memory_ds=None, **kwargs):
        self.filename = fn
        self.load_args = args
        self.load_kwargs = kwargs

        # _ds and _on_disk here (and below) are mainly for testing purposes so
        # that in-memory datasets can be added to the data store.
        self._ds = in_memory_ds
        self._on_disk = in_memory_ds is None

    @contextlib.contextmanager
    def load(self):
        if self._on_disk:
            ds = yt.load(self.filename, *self.load_args, **self.load_kwargs)
        else:
            ds = self._ds

        try:
            yield ds
        finally:
            if self._on_disk:
                # ds.close doesnt do anything for majority of frontends... might
                # as well call it though.
                ds.close()
            # do nothing if the ds is in-memory.

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

    def store(self, fn: str, dataset_name: Optional[str] = None, in_memory_ds=None):
        """
        A function to track all dataset.
        Stores dataset name, or if no name is provided,
        adds a number as the name.
        """
        dataset_name = self.validate_name(fn, dataset_name)

        if dataset_name not in self.available_datasets:
            self.available_datasets[dataset_name] = DatasetContext(
                fn, in_memory_ds=in_memory_ds
            )

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
