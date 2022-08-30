import argparse

from analysis_schema._workflows import MainWorkflow


def load_and_run(json_file):
    """
    A function to load the user JSON and load it into the analysis schema model, and
    the run that model to produce an output.

    Args:
        json_file (json file): the JSON users edit
    """

    wk = MainWorkflow(json_file)
    return wk.run_all()


if __name__ == "__main__":

    # create a parser
    parser = argparse.ArgumentParser(description="Handling Filenames for Analysis")

    # add the JSON file name agrument
    parser.add_argument("JSONFile", help="Call the JSON with the Schema to run")

    args = parser.parse_args()

    # run the analysis
    load_and_run(args.JSONFile)
