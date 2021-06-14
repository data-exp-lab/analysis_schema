import json
from main import analysis_model
import pydantic

# This code will save the model to a json file, which will be referenced by the user

with open("pydantic_schema_file.json", "w") as file:
    file.write(analysis_model.schema_json(indent=2))