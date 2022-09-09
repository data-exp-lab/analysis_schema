import json
import os

import pytest

from analysis_schema import _testing as sch_testing
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
        if sch_testing.yt_file_exists(dsfi) is False:
            pytest.skip(f"{dsfi} not found.")

    # get a new workflow with the updated dictionary
    newdict = sch_testing.read_and_adjust_plot_dir(tmpdir, jfi)
    wkflow = MainWorkflow(newdict)

    # actually run it and check that the figures exist
    for output in wkflow.run_all():
        output_name = list(output.keys())[0]
        output_fi = output[output_name]
        assert os.path.isfile(str(output_fi))


def test_execution_with_fake_ds(tmpdir):
    jfi = "analysis_schema/pydantic_schema_example.json"
    newdict = sch_testing.read_and_adjust_plot_dir(tmpdir, jfi)

    # get a new workflow with the updated dictionary
    flist = [("gas", "density"), ("gas", "temperature")]
    ulist = ["g/cm**3", "K"]
    wkflow = MainWorkflow(newdict)
    wkflow = sch_testing.force_in_mem_dstore(wkflow, field_list=flist, units_list=ulist)

    # actually run it and check that the figures exist
    for output in wkflow.run_all():
        output_name = list(output.keys())[0]
        output_fi = output[output_name]
        assert os.path.isfile(str(output_fi))


bad_wkflows = []
for fi in os.listdir("tests"):
    if "wkflow_" in fi and fi.endswith("error.json"):
        bad_wkflows.append(os.path.join("tests", fi))


@pytest.mark.parametrize("jfi", bad_wkflows)
def test_bad_ds_referencing(jfi):
    with pytest.raises(ValueError):
        _ = MainWorkflow(jfi)
