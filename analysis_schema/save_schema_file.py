from .schema_model import ytModel

# This code will save an empty (no values have been entered) model to a json file
# which will be referenced by the user


def save_schema(fi: str = None):
    """
    A function to create a schema file
    """

    analysis_model_schema = ytModel(
        Data=[{"DatasetName": "", "FileName": ""}], Plot=[{}]
    )

    if fi is None:
        fi = "../analysis_schema/yt_analysis_schema.json"

    with open(fi, "w") as file:
        file.write(analysis_model_schema.schema_json(indent=2))

    print("Schema has been saved!")
