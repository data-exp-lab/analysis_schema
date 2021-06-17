import json
from analysis_schema.BaseModelFunctions import show_plots
from analysis_schema.SchemaModel import ytModel
import sys
import argparse 

def load_and_run(json_file):
    # open the file where the user is entering values
    live_json = open(json_file)
    # assign to a variable
    live_schema = json.load(live_json)
    live_json.close()
    # remove schema line
    live_schema.pop('$schema')
    # create analysis schema model
    analysis_model = ytModel(Plot = 
        live_schema['Plot']
    )
    print(show_plots(analysis_model))

if __name__ == "__main__":

    # create a parser
    parser = argparse.ArgumentParser(description='Handling Filenames for Analysis')
    
    # add the JSON file name agrument
    parser.add_argument('JSONFile',
                    help='Call the JSON with the Schema to run')
    
    args = parser.parse_args()

    # run the analysis
    load_and_run(args.JSONFile)

   