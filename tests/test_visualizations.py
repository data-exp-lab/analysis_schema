import os

import pytest

from analysis_schema import _testing as sch_testing
from analysis_schema._workflows import MainWorkflow

json_viz_files = []
for fi in os.listdir("tests"):
    if "viz_" in fi and fi.endswith("json"):
        json_viz_files.append(os.path.join("tests", fi))


@pytest.mark.parametrize("jfi", json_viz_files)
def test_viz_jsons(tmpdir, jfi):

    newdict = sch_testing.read_and_adjust_plot_dir(tmpdir, jfi)

    # get a new workflow with the updated dictionary
    flist = [("gas", "density"), ("gas", "temperature")]
    ulist = ["g/cm**3", "K"]
    wkflow = MainWorkflow(newdict)
    wkflow = sch_testing.force_in_mem_dstore(wkflow, field_list=flist, units_list=ulist)

    # actually run it and check that the figures exist
    for output in wkflow.run_all():
        for viz_title, viz_paths in output.items():
            if isinstance(viz_paths, list):
                for output_fi in viz_paths:
                    assert os.path.isfile(str(output_fi))
            else:
                assert os.path.isfile(str(viz_paths))
