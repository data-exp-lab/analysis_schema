import json
import os

import pytest
from yt.testing import fake_amr_ds

from analysis_schema._data_store import DataStore
from analysis_schema._testing import yt_file_exists
from analysis_schema._workflows import MainWorkflow


def test_workflow_instantiation():
    jfi = "analysis_schema/pydantic_schema_example.json"
    _ = MainWorkflow(jfi)

    with open(jfi) as jstream:
        jdict = json.loads(jstream.read())
    _ = MainWorkflow(jdict)


def test_full_execution(tmpdir):
    jfi = "analysis_schema/pydantic_schema_example.json"

    # first check if the files for the workflow are available
    init_wkflow = MainWorkflow(jfi)
    files_used = []
    for dscontext in init_wkflow.data_store.available_datasets.values():
        files_used.append(dscontext.filename)

    for dsfi in files_used:
        if yt_file_exists(dsfi) is False:
            pytest.skip(f"{dsfi} not found.")

    # adjust the output files so they will write to a temporary directory
    with open(jfi) as jstream:
        jdict = json.loads(jstream.read())

    newdict = jdict.copy()
    for iplot, p in enumerate(jdict["Plot"]):
        ptype = list(p.keys())[0]
        p[ptype]["output_dir"] = str(tmpdir)
        newdict["Plot"][iplot] = p

    # get a new workflow with the updated dictionary
    wkflow = MainWorkflow(newdict)

    # actually run it and check that the figures exist
    for output in wkflow.run_all():
        output_name = list(output.keys())[0]
        output_fi = output[output_name]
        assert os.path.isfile(str(output_fi))


def test_execution_with_fake_ds(tmpdir):
    jfi = "analysis_schema/pydantic_schema_example.json"

    # adjust the output files so they will write to a temporary directory
    with open(jfi) as jstream:
        jdict = json.loads(jstream.read())

    newdict = jdict.copy()

    for iplot, p in enumerate(jdict["Plot"]):
        ptype = list(p.keys())[0]
        p[ptype]["output_dir"] = str(tmpdir)
        newdict["Plot"][iplot] = p

    # get a new workflow with the updated dictionary
    wkflow = MainWorkflow(newdict)

    # replace the data store datasets with in-memory datasets
    new_store = DataStore()
    flist = [("gas", "density"), ("gas", "temperature")]
    ulist = ["g/cm**3", "K"]
    for dsname, dscon in wkflow.data_store.available_datasets.items():
        ds_ = fake_amr_ds(fields=flist, units=ulist)
        new_store.store(dscon.filename, dataset_name=dsname, in_memory_ds=ds_)
    wkflow.data_store = new_store

    # actually run it and check that the figures exist
    for output in wkflow.run_all():
        output_name = list(output.keys())[0]
        output_fi = output[output_name]
        assert os.path.isfile(str(output_fi))
