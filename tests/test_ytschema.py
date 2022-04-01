# isort: skip_file
import json

import yt
from yt.testing import fake_amr_ds

import analysis_schema
from analysis_schema._data_store import dataset_fixture
from analysis_schema.base_model import (
    _check_run,
    ytBaseModel,
    ytDataObjectAbstract,
    ytParameter,
)

ds_only = r"""
{
    "$schema": "./yt_analysis_schema.json",
    "Data": [
      {
      "FileName": "IsolatedGalaxy/galaxy0030/galaxy0030",
      "DatasetName": "IG_Testing"
    }
  ]
}
"""


viz_only_prj = r"""
{
    "$schema": "./yt_analysis_schema.json",
    "Plot": [
      {
        "ProjectionPlot": {
          "Axis":"y",
          "FieldNames": {
            "field": "temperature",
            "field_type": "gas"
          },
          "DataSource": {
            "region": {
              "center": [0.25, 0.25, 0.25],
              "left_edge": [0.0, 0.0, 0.0],
              "right_edge": [0.5, 0.5, 0.5]
            }
          }
        }
      }
    ]
}
"""


viz_only_slc = r"""
{
    "$schema": "./yt_analysis_schema.json",
    "Plot": [
      {
        "SlicePlot": {
          "Axis":"y",
          "FieldNames": {
            "field": "temperature",
            "field_type": "gas"
          },
          "DataSource": {
            "sphere": {
              "Center": [0.25, 0.25, 0.25],
              "Radius": 0.25
            }
          }
        }
      }
    ]
}
"""


def test_validation():

    # only testing the validation here, not instantiating yt objects
    model = analysis_schema.ytModel.parse_raw(ds_only)
    jdict = json.loads(ds_only)
    assert str(model.Data[0].fn) == jdict["Data"][0]["FileName"]


def test_execution():

    # we can inject an instantiated dataset here! the methods that require a
    # ds will check the dataset store if ds is None and use this ds:
    test_ds = fake_amr_ds(fields=[("gas", "temperature")], units=["K"])
    dataset_fixture._instantiated_datasets["_test_ds"] = test_ds

    # run the slice plot
    model = analysis_schema.ytModel.parse_raw(viz_only_slc)
    m = model._run()
    print(m)
    assert isinstance(m[0], yt.AxisAlignedSlicePlot)

    # run the projection plot
    model = analysis_schema.ytModel.parse_raw(viz_only_prj)
    m = model._run()
    print(m)
    assert isinstance(m[0], yt.ProjectionPlot)


def test_base_model():
    # some basic tests of base_model
    for cls in [ytBaseModel, ytDataObjectAbstract, ytParameter]:
        c = cls()
        assert _check_run(c)
    assert _check_run("someothertype") is False
