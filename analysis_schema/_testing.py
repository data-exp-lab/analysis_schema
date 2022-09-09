import json
import os

from yt.config import ytcfg
from yt.testing import fake_amr_ds

from analysis_schema._data_store import DataStore


def yt_file_exists(req_file):
    # returns True if yt can find the file, False otherwise (a simplification of
    # yt.testing.requires_file without the nose dependency)
    path = ytcfg.get("yt", "test_data_dir")

    if os.path.exists(req_file):
        return True
    else:
        if os.path.exists(os.path.join(path, req_file)):
            return True
    return False


def force_in_mem_dstore(wkflow, field_list: list = None, units_list: list = None):
    # replace the data store datasets with in-memory datasets
    new_store = DataStore()
    if field_list is None:
        field_list = [("gas", "density"), ("gas", "temperature")]
        units_list = ["g/cm**3", "K"]
    for dsname, dscon in wkflow.data_store.available_datasets.items():
        ds_ = fake_amr_ds(fields=field_list, units=units_list)
        new_store.store(dscon.filename, dataset_name=dsname, in_memory_ds=ds_)
    wkflow.data_store = new_store
    return wkflow


def inject_tmpdir_to_plots(tmpdir, jdict: dict, newdict: dict) -> dict:
    # adjusts the output directory of all plots to be tmpdir
    for iplot, p in enumerate(jdict["Plot"]):
        ptype = list(p.keys())[0]
        p[ptype]["output_dir"] = str(tmpdir)
        newdict["Plot"][iplot] = p
    return newdict


def read_and_adjust_plot_dir(tmpdir, jfi) -> dict:
    # returns the json file as a dict will all plots adjsuted to write to tmpdir
    with open(jfi) as jstream:
        jdict = json.loads(jstream.read())
    return inject_tmpdir_to_plots(tmpdir, jdict, jdict.copy())
