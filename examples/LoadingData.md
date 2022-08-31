
# Loading Data

The most basic task you can do in the analysis schema is load your data. This is done by calling the keyword `Data` and filling out the `FileName` and `DatasetName` attributes. The `FileName`  is the file or file path for your data and the `DatasetName` is the name (in the form of a string) for your data, similar to a variable name. 

The `Data` keyword is a list data type, so you can specify multiple datasets within a workflow. 

## Loading a Single Dataset

A single dataset:

```json

{
    "$schema": "../analysis_schema/yt_analysis_schema.json",
    "Data": [
        {
            "FileName": "IsolatedGalaxy/galaxy0030/galaxy0030",
            "DatasetName": "Galaxy"
        }
    ]
}

```

## Loading Multiple Datasets

Mulitple datasets in a list:

```json

{
    "$schema": "../analysis_schema/yt_analysis_schema.json",
    "Data": [
        {
            "FileName": "IsolatedGalaxy/galaxy0030/galaxy0030",
            "DatasetName": "Galaxy"
        },
        {
            "FileName": "enzo_tiny_cosmology/DD0000/DD0000",
            "DatasetName": "Enzo"
        }
    ]
  }

```

## Flexible Order of Operations

You can declare your dataset at the top of the document, or you can describe other aspects of the workflow and fill in the data further down. You can describe a plot and specify the data within that description:

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

Both the `Plot` and `Data` keywords support lists, so you can specify multiple plots and datasets and the analysis schema will iterate through each specification and plot each dataset you specify. 