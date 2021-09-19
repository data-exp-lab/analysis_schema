import json

import yt
from yt.testing import assert_array_equal

import analysis_schema

plot_ds = r"""
{
    "$schema": "./yt_analysis_schema.json",
    "Data": [{
       "FileName": "IsolatedGalaxy/galaxy0030/galaxy0030",
       "DatasetName": "IG_Testing"
           }
   }]
 }
"""


def test_validation():

    # only testing the validation here, not instantiating yt objects
    model = analysis_schema.ytModel.parse_raw(plot_ds)
    jdict = json.loads(plot_ds)
    assert str(model.Data[0].fn) == jdict["Data"][0]["FileName"]


def test_execution():

    # requires the datafile -- should use pytest to decorate or use an in-mem
    # dataset (which the current model does not support).
    model = analysis_schema.ytModel.parse_raw(plot_ds)

    try:
        ds = yt.load(model.Data[0].fn)
        file_exists = True
    except FileNotFoundError:
        file_exists = False

    domain_attrs = ["center", "width", "dimensions", "left_edge", "right_edge"]
    if file_exists:
        ds_a = model.Data[0]._run()

        # check that domain attributes match
        for attr in domain_attrs:
            d_name = "domain_" + attr
            assert_array_equal(getattr(ds_a, d_name), getattr(ds, d_name))

        # check that field list matches
        flds_a = ds_a.field_list
        flds = ds.field_list
        assert all([fld in flds_a for fld in flds])
