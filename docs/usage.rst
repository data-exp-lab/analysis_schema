=====
Usage
=====

Using the analysis schema simply requires using the `ytModel` class and describing a workflow by selecting the relevant keyword and entering a value. The schema will validate what you have entered, and then run the code and return an output. This is very similar to using a JSON document, which is made up key-value pairs. In fact, the Analysis Schema is built and run using `pydantic`, a library that creates and validates models in JSON format. 

insert gif

Quickstart
-----------

The Analysis Schema can be used in both an interactive environment, like Jupyter, or in the command line.  

Getting Started in Jupyter:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To use Analysis Schema in a Jupyter environment::

    import analysis_schema

    # this is the model, where you can enter your workflow
    # this example includes the creation of a two dimensional plot called a SlicePlot
    # The keyword `SlicePlot` is called and the relevant information is entered to create the plot, such as the data, the axis, and the field to plot from the data

    model = analysis_schema.ytModel(Plot=[
                         {
                            "SlicePlot": {
                                "Dataset": {
                                    "FileName": "../yt_JSON_Schema/IsolatedGalaxy/galaxy0030/galaxy0030",
                                    "DatasetName": "IG"
                                },
                                "Axis":"x",
                                "FieldName": {
                                       "field": "density"
                                   }
                                   
                               }
                            }
                        ]
                    )

    # the model can be printed out in JSON format
    print(model.json())

    # the model has been created from the above workflow, and now it can be plotted by calling the 
    # ``show_plots`` function
    #In a Jupyter environment, you can use the argument `display_inline=True`
    # This will take the model and run the code and return the output which is a SlicePlot

    sliceplot = analysis_schema.BaseModelFunctions.show_plots(schema=model, display_inline=True)

Getting Started in the Command Line:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Analysis Schema Model
---------------------