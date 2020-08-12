import analysis_schema
import json

ex_ds1_json = r"""
{
    "domain_left_edge": {
        "values": [0.0, 0.0, 0.0],
        "unit": "unitary"
    },
    "domain_right_edge": {
        "values": [1.0, 1.0, 1.0],
        "unit": "unitary"
    },
    "domain_dimensions": [256, 256, 256],
    "current_time": {
        "value": 1.0,
        "unit": "year"
    },
    "geometry": "cartesian",
    "dataset_type": "braaaaainz",
    "domain_contexts": []
}
"""

ex_ds2_json = r"""
{
    "domain_left_edge": [
        [0.0, 0.0, 0.0],
        "unitary"
    ],
    "domain_right_edge": [
        [1.0, 1.0, 1.0],
        "unitary"
    ],
    "domain_dimensions": [256, 256, 256],
    "current_time": [ 1.0, "year" ],
    "geometry": "cartesian",
    "dataset_type": "braaaaainz",
    "domain_contexts": []
}
"""

def test_dataset_specifications():
    ds1 = analysis_schema.Dataset.parse_raw(ex_ds1_json)
    ds2 = analysis_schema.Dataset.parse_raw(ex_ds2_json)
    assert ds1.domain_left_edge.unit == "unitary"
    analysis_schema.Dataset.validate(json.loads(ex_ds1_json))
    analysis_schema.Dataset.validate(json.loads(ex_ds2_json))
