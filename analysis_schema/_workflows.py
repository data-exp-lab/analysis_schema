import abc
import os
from pathlib import PosixPath
from typing import Union

from ._data_store import DataStore
from ._model_instantiation import _is_yt_schema_instance, yt_registry
from .data_classes import Dataset
from .schema_model import ytModel


class BaseWorkflow:
    def __init__(self, model, ds_name=None):
        self.model = model
        self.ds_name = ds_name

    @abc.abstractmethod
    def run(self):
        pass


class Workflow(BaseWorkflow):
    def run(self, ds=None):
        runner = yt_registry.get(self.model)
        return runner.run(self.model, ds=ds)


class MainWorkflow:
    def __init__(self, json_like: Union[str, PosixPath, dict]):

        self.model: ytModel = self._validate_json(json_like)
        self.data_store = DataStore()
        self.workflows_by_dataset = {}
        self.workflows_with_no_dataset = []
        self.build_workflows()

    def _validate_json(self, json_like: Union[str, PosixPath, dict]):

        if isinstance(json_like, str):
            # could be a file or a string
            if os.path.isfile(json_like):
                model = ytModel.parse_file(json_like)
            else:
                # might be a json string, try to parse it
                model = ytModel.parse_raw(json_like)
        elif isinstance(json_like, PosixPath):
            model = ytModel.parse_file(json_like)
        else:
            model = ytModel.parse_obj(json_like)
        return model

    def build_workflows(self):

        # first add the dataset definitions to the store
        if self.model.Data is not None:
            for datamodel in self.model.Data:
                _check_for_ds(datamodel, set(), self.data_store)

        # assemble workflows, potentially adding more datasets to store
        workflows_by_ds = {}
        workflows_without_dataset = []
        if (
            self.model.Plot is not None
        ):  # could generalize this for other high-level schema objects
            for plot in self.model.Plot:
                dataset_names = _check_for_ds(plot, set(), self.data_store)
                ds_list = list(dataset_names)  # the datasets used by this workflow
                if len(ds_list) > 0:
                    for dsname in ds_list:
                        # can specify multiple datasets to signal that a workflow should
                        # be run for each dataset, so duplicate the workflow for each
                        # dataset
                        if dsname not in workflows_by_ds:
                            workflows_by_ds[dsname] = []
                        workflows_by_ds[dsname].append(Workflow(plot, dsname))
                else:
                    # nothing would end up here at present (ever?)
                    workflows_without_dataset.append(Workflow(plot))

        self.workflows_by_dataset = workflows_by_ds
        self.workflows_with_no_dataset = workflows_without_dataset

    def run_all(self):
        output = []

        # potential for parallel execution here...
        for dsname, workflows in self.workflows_by_dataset.items():
            ds_context = self.data_store.retrieve(dsname)
            with ds_context.load() as ds:
                for workflow in workflows:
                    output.append(workflow.run(ds))

        for workflow in self.workflows_with_no_dataset:
            # should be empty...
            output.append(workflow.run())
        return output


def _add_ds_to_store(pydantic_ds: Dataset, data_store):
    ds_nm = pydantic_ds.DatasetName
    fn = pydantic_ds.fn
    data_store.store(fn, dataset_name=ds_nm)
    name_to_add = data_store.validate_name(fn, ds_nm)
    return name_to_add


def _check_for_ds(model, dataset_set: set, data_store):
    # walk a pydantic model and add datasets to the data store
    # returns a set of the datasets by short name

    if isinstance(model, Dataset):
        name_to_add = _add_ds_to_store(model, data_store)
        dataset_set.update((name_to_add,))
    elif _is_yt_schema_instance(model):
        for attr in model.__fields__.keys():
            attval = getattr(model, attr)
            if _is_yt_schema_instance(attval):
                dataset_set = _check_for_ds(attval, dataset_set, data_store)
            elif isinstance(attval, list) and len(attval):
                if _is_yt_schema_instance(attval[0]):
                    for val in attval:
                        dataset_set = _check_for_ds(val, dataset_set, data_store)

    return dataset_set
