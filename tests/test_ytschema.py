# isort: skip_file
import json

from analysis_schema.schema_model import ytModel

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


more_complete_example = r"""
{
  "$schema": "../analysis_schema/yt_analysis_schema.json",
  "Data": [
    {
        "FileName": "IsolatedGalaxy/galaxy0030/galaxy0030",
        "DatasetName": "IG_Testing"
    }
   ],
  "Plot": [
    {
      "ProjectionPlot": {
        "Dataset": [
          {
            "FileName": "great_filename",
            "DatasetName": "nice"
          },
          {
            "FileName": "and_another",
            "DatasetName": "another"
          }
        ],
        "Axis":"y",
        "Fields": {
          "field": "density",
          "field_type": "gas"
        },
        "WeightFieldName": {
          "field": "temperature",
          "field_type": "gas"
        },
        "output_type": "file"
      }
    }
  ]
}
"""


def test_validation():

    # only testing the validation here, not instantiating yt objects
    model = ytModel.parse_raw(ds_only)
    jdict = json.loads(ds_only)
    assert str(model.Data[0].fn) == jdict["Data"][0]["FileName"]

    model = ytModel.parse_raw(more_complete_example)
    jdict = json.loads(ds_only)
    assert str(model.Data[0].fn) == jdict["Data"][0]["FileName"]
    assert str(model.Plot[0].ProjectionPlot.normal) == "y"
