from .schema_model import ytModel

# This code will save an empty (no values have been entered) model to a json file
# which will be referenced by the user
analysis_model_schema = ytModel(Data=[{"FileName": "", "DatasetName": ""}], Plot=[{}])

with open("analysis_schema/yt_analysis_schema.json", "w") as file:
    file.write(analysis_model_schema.schema_json(indent=2))

print("Schema is has been saved!")
