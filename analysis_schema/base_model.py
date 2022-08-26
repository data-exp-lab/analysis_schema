from pydantic import BaseModel


def show_plots(schema, files):
    """
    This function accepts the schema model and runs it using yt code which returns
    a list. This function iterates through the list and displays each output.

    Args:
        schema ([dict]): the analysis schema filled out with yt specificaions
    """
    result = schema._run()
    print("The result:", result)
    for output in range(len(tuple(result))):
        print("each output:", result[output])
        if files == "Jupter":
            result[output].show()
        if files != "Jupyter":
            result[output].save()
            print("Files with output have been created!")


class ytBaseModel(BaseModel):
    pass
