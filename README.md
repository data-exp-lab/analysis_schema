# Analysis Schema

A declarative schema and workflow framework for analysis and visualization of physical systems.

The Analysis Schema creates a workflow system that processes a configuration file where users specify _what_ they would like the code to do, instead of _how_ to do it to complete analysis and visualization tasks. It supports high level analysis description that can be saved, shared, and reused in JSON document. 

It consists of three pieces:

1. A structured schema that guides the workflow. See the `yt_analysis_schema.json`. 
2. An engine that connects input from the configuration file to the underlying code.
3. The configuration file. 

## Example

Use a JSON file to describe a basic plot. The file has to reference the structured schema file, which is also called the analysis schema. The schema validates the workflow and ensures the correct data types are used.

Let's call this `example.py` and fill it out:

```JSON

{
    "$schema": "yt_analysis_scheam.json",
    "Plot": [
        {
            "ProjectionPlot": {
                "Dataset": [
                    {
                        "Filename": "IsolatedGalaxy/galaxy0030/galaxy0030",
                        "DatasetName": "IG"
                    }
                ],
                "Axis": "y",
                "FieldNames": {
                    "field": "density",
                    "field_type": "gas"
                }
            }
        }
    ]
}

```

Once a configuraion file is complete, the file can be submitted as parameter to the program where the engine executes the code. The `run_analysis` module executes the code:

```
python3 run_analysis.py example.py
```

After running that line of code in the command line, image files of a projection plot or other visauls are returned.

Documentation is coming soon to: https://analysis-schema.readthedocs.io.

## Dependencies

Currently, the Analysis Schema is built from [yt](https://github.com/yt-project/yt), a python library for analyzing and visauliation volumetric data. It also uses [pydantic](https://github.com/pydantic/pydantic) to create the schema and validate workflow input.

[![yt-project](https://img.shields.io/static/v1?label="works%20with"&message="yt"&color="blueviolet")](https://yt-project.org)

The Analysis Schema requires Python 3.7+ and yt 4.0 in addition to other packages.

## License

* Free software: MIT license
