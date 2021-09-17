import argparse
import json

from analysis_schema.BaseModelFunctions import show_plots
from analysis_schema.SchemaModel import ytModel


def load_and_run(json_file, files):
    """
    A function to load the user JSON and load it into the analysis schema model, and
    the run that model to produce an output.

    Args:
        json_file (json file): the JSON users edit
    """
    # open the file where the user is entering values
    live_json = open(json_file)
    # assign to a variable
    live_schema = json.load(live_json)
    live_json.close()
    # remove schema line
    live_schema.pop("$schema")
    # create analysis schema model
    if "Data" in live_schema.keys():
        analysis_model = ytModel(Data=live_schema["Data"], Plot=live_schema["Plot"])
    else:
        analysis_model = ytModel(Plot=live_schema["Plot"])
    print(show_plots(analysis_model, files))


if __name__ == "__main__":

    # create a parser
    parser = argparse.ArgumentParser(description="Handling Filenames for Analysis")

    # add the JSON file name agrument
    parser.add_argument("JSONFile", help="Call the JSON with the Schema to run")

    parser.add_argument(
        "ImageFormat",
        nargs="*",
        help="Enter 'Jupyter' to run .show() or a filename to run .save()",
    )

    args = parser.parse_args()

    # run the analysis
    load_and_run(args.JSONFile, args.ImageFormat)
