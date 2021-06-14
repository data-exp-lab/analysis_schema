from BaseModelFunctions import ytBaseModel
from typing import List
from ytDataClasses import Visualizations


class ytModel(ytBaseModel):
    '''
    Create a model in the form of a json schema, using the yt data classes. As values are added to the file referencing the schema, the function `run` with be called recursively to acccess nested yt elements and run the yt code. 

    The run function iterates through the attributes of the class and runs this values entered for those attributes and puts the output into a list. This list will be iterated through to render and display the output. 
    '''
    Plot: List[Visualizations]

    class Config:
        title = 'yt Schema Model for Descriptive Visualization and Analysis'
        underscore_attrs_are_private = True
    
    def _run(self):
        # for the top level model, we override this. Nested objects will still be recursive!
        output_list = list()
        att = getattr(self, "Plot")
        for p in att:
            for attribute in dir(p):
                if attribute.endswith('Plot'):
                    new_att = getattr(p, attribute)
                    if new_att is not None:
                        output_list.append(new_att._run())
            return output_list

