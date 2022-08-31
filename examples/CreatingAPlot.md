# Creating a Plot

You can quickly create a plot with minimal description. The output is return as an image file. 

## SlicePlot

```json

{
    "$schema": "../analysis_schema/yt_analysis_schema.json",
    "Plot": [
        {
            "SlicePlot": {
                "Axis": "x",
                "FieldNames": {
                    "field": "density",
                    "field_type": "gas"
                },
                "Dataset": [
                    {
                        "FileName": "IsolatedGalaxy/galaxy0030/galaxy0030",
                        "DatasetName": "IG"
                    }
                ],
                "output_type": "file"
            }
        }
    ]
  }

```


## ProjectionPlot

You can specify more than one dataset within a plot. In this case two projection plots are created, one for each dataset specified. 

```json
{
    "$schema": "../analysis_schema/yt_analysis_schema.json",
    "Plot": [
        {
            "ProjectionPlot": {
                "Dataset": [
                    {
                        "FileName": "IsolatedGalaxy/galaxy0030/galaxy0030",
                        "DatasetName": "IG"
                    },
                    {
                        "FileName": "enzo_tiny_cosmology/DD0000/DD0000",
                        "DatasetName": "Enzo"
                    }
                ],  
                "Axis": "z",
                "FieldNames": {
                    "field": "density",
                    "field_type": "gas"
                },
                "WeightFieldName": {
                    "field": "pressure",
                    "field_type": "gas"
                },
                "output_type": "file"
            }
        }
    ]
  }

```

