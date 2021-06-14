import json
from BaseModelFunctions import show_plots
from SchemaModel import ytModel

# open the file where the user is entering values
live_json = open("schema_instance.json")
# assign to a variable
live_schema = json.load(live_json)
live_json.close()
# remove schema line
live_schema.pop('$schema')

# create analysis schema model
analysis_model = ytModel(Plot = 
    live_schema['Plot']
)

# print file output
print(show_plots(analysis_model))