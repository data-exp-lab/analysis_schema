from inspect import getfullargspec
from typing import List, Optional

import yt
from pydantic import BaseModel

from ._data_store import DatasetFixture


def show_plots(schema, files):
    """
    This function accepts the schema model and runs it using yt code which returns
    a list. This function iterates through the list and displays each output.

    Args:
        schema ([dict]): the analysis schema filled out with yt specificaions
    """
    result = schema._run()
    print(result)
    for output in range(len(tuple(result))):
        print("each output:", result[output])
        if files == "Jupter":
            result[output].show()
        if files != "Jupyter":
            result[output].save()
            print("Files with output have been created!")


class ytBaseModel(BaseModel):
    """
    A class to connect attributes and their values to yt operations and their
    keyword arguments.

    Args:
        BaseModel ([type]): A pydantic basemodel in the form of a json schema

    Raises:
        AttributeError: [description]

    Returns:
        [list]: A list of yt classes to be run and then displayed
    """

    _arg_mapping: dict = {}  # mapping from internal yt name to schema name
    _yt_operation: Optional[str]
    _known_kwargs: Optional[List[str]] = None  # a list of known keyword args

    def _run(self):

        # the list that we'll use to eventually call our function
        the_args = []
        # this method actually executes the yt code

        # first make sure yt is imported and then get our function handle. This assumes
        # that our class name exists in yt's top level api.
        import yt

        funcname = getattr(self, "_yt_operation", type(self).__name__)
        # if the function is not readily available in yt, move to the except block
        # try:
        func = getattr(yt, funcname)

        # now we get the arguments for the function:
        # func_spec.args, which lists the named arguments and keyword arguments.
        # ignoring vargs and kw-only args for now...
        # see https://docs.python.org/3/library/inspect.html#inspect.getfullargspec
        func_spec = getfullargspec(func)

        # the argument position number at which we have default values (a little
        # hacky, should be a better way to do this, and not sure how to scale it to
        # include *args and **kwargs)
        n_args = len(func_spec.args)  # number of arguments
        if func_spec.defaults is None:
            # no default args, make sure we never get there...
            named_kw_start_at = n_args + 1
        else:
            # the position at which named keyword args start
            named_kw_start_at = n_args - len(func_spec.defaults)

        # loop over the call signature arguments and pull out values from our pydantic
        # class. this is recursive! will call _run() if a given argument value is also
        # a ytBaseModel.
        for arg_i, arg in enumerate(func_spec.args):
            # check if we've remapped the yt internal argument name for the schema
            if arg in ["self", "cls"]:
                continue

            # get the value for this argument. If it's not there, attempt to set default
            # values for arguments needed for yt but not exposed in our pydantic class
            try:
                arg_value = getattr(self, arg)
                if arg_value is None:
                    default_index = arg_i - named_kw_start_at
                    arg_value = func_spec.defaults[default_index]
            except AttributeError:
                if arg_i >= named_kw_start_at:
                    # we are in the named keyword arguments, grab the default
                    # the func_spec.defaults tuple 0 index is the first named
                    # argument, so need to offset the arg_i counter
                    default_index = arg_i - named_kw_start_at
                    arg_value = func_spec.defaults[default_index]
                else:
                    raise AttributeError(f"could not file {arg}")

            if _check_run(arg_value):
                arg_value = arg_value._run()
            the_args.append(arg_value)

        # if this class has a list of known kwargs that we know will not be
        # picked up by argspec, add them here. Not using inspect here because
        # some of the yt visualization classes pass along kwargs, so we need
        # to do this semi-manually for some classes and functions.
        kwarg_dict = {}
        if self._known_kwargs:
            for kw in self._known_kwargs:
                arg_value = getattr(self, kw, None)
                if _check_run(arg_value):
                    arg_value = arg_value._run()
                kwarg_dict[kw] = arg_value

        return func(*the_args, **kwarg_dict)


def _check_run(obj) -> bool:
    # the following classes will have a ._run() attribute that needs to be called
    if (
        isinstance(obj, ytBaseModel)
        or isinstance(obj, ytParameter)
        or isinstance(obj, ytDataObjectAbstract)
    ):
        return True
    return False


class ytParameter(BaseModel):
    _skip_these = ["comments"]

    def _run(self):
        p = [
            getattr(self, key)
            for key in self.schema()["properties"].keys()
            if key not in self._skip_these
        ]
        if len(p) > 1:
            raise ValueError("ytParameter instances can only have single values")
        return p[0]


class ytDataObjectAbstract(ytBaseModel):
    # abstract class for all the data selectors to inherit from

    def _run(self):
        from yt.data_objects.data_containers import data_object_registry

        the_args = []
        funcname = getattr(self, "_yt_operation", type(self).__name__)

        # get the function from the data object registry
        val = data_object_registry[funcname]

        # iterate through the arguments for the found data object
        for arguments in val._con_args:
            con_value = getattr(self, arguments)
            # check that the argument is the correct instance
            if isinstance(con_value, ytDataObjectAbstract):
                # call the _run() function on the agrument
                con_value = con_value._run()
            the_args.append(con_value)

        # if there is a dataset sitting in _instantiated_datasets, add it to
        # the args and call as a keyword argument

        # if len(Dataset_Fixture.all_data) > 0:
        #     ds_keys = list(Dataset_Fixture.all_data.keys())
        #     for key in ds_keys:
        #         ds = yt.load(Dataset_Fixture.all_data[key])
        #         return val(*the_args, ds=ds)
        # else:
        #     raise AttributeError(
        #         "could not find a dataset: cannot build the data container"
        #     )


        if len(_instantiated_datasets) > 0:
            ds_keys = list(_instantiated_datasets.keys())
            ds = _instantiated_datasets[ds_keys[0]]
            return val(*the_args, ds=ds)
        else:
            raise AttributeError(
                "could not find a dataset: cannot build the data container"
            )
