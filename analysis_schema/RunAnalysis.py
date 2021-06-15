import json
from .BaseModelFunctions import show_plots
from .SchemaModel import ytModel
import sys
 
# total arguments
n = len(sys.argv)
print("Total arguments passed:", n)
 
# Arguments passed
print("\nName of Python script:", sys.argv[0])
 
print("\nArguments passed:", end = " ")
for i in range(1, n):
    print(sys.argv[i], end = " ")

# open the file where the user is entering values
live_json = open(sys.argv[1])
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