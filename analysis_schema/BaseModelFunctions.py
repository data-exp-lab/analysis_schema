from pydantic import BaseModel, Field, constr
from typing import Optional
from inspect import getfullargspec

def show_plots(schema):
    """This function accepts the schema model and runs it using yt code which returns a list. This function iterates through the list and displays each output. 

    Args:
        schema ([dict]): the analysis schema filled out with yt specificaions
    """
    result = schema._run()
    print(result)
    for output in range(len(tuple(result))):
        print("each output:", result[output])
        result[output].show()


class ytBaseModel(BaseModel):
    """A class to connect attributes and their values to yt operations and their keywork arguements. 

    Args:
        BaseModel ([type]): A pydantic basemodel in the form of a json schema

    Raises:
        AttributeError: [description]

    Returns:
        [list]: A list of yt classes to be run and then displayed
    """
    _arg_mapping: dict = {}  # mapping from internal yt name to schema name
    _yt_operation: Optional[str]
    # the list to store the data after it has been instaniated
    _data_source = {}
    
    def _run(self):

         # the list that we'll use to eventually call our function
        the_args = []
        # this method actually executes the yt code
        
    

        # first make sure yt is imported and then get our function handle. This assumes
        # that our class name exists in yt's top level api.
        import yt

        print(self._yt_operation)
        funcname = getattr(self, "_yt_operation", type(self).__name__)
        print("found name:", funcname)

        # if the function is not readily available in yt, move to the except block
        # try:
        func = getattr(yt, funcname)
        print(f"pulled func {func}", type(func))
                    

        # now we get the arguments for the function:
        # func_spec.args, which lists the named arguments and keyword arguments.
        # ignoring vargs and kw-only args for now...
        # see https://docs.python.org/3/library/inspect.html#inspect.getfullargspec
        func_spec = getfullargspec(func)
        print("spec", func_spec)

        # the argument position number at which we have default values (a little hacky, should
        # be a better way to do this, and not sure how to scale it to include *args and **kwargs)
        n_args = len(func_spec.args)  # number of arguments
        print("number of args:", n_args)
        if func_spec.defaults is None:
            # no default args, make sure we never get there...
            named_kw_start_at = n_args + 1
        else:
            # the position at which named keyword args start
            named_kw_start_at = n_args - len(func_spec.defaults)
        print(f"keywords start at {named_kw_start_at}")

        # loop over the call signature arguments and pull out values from our pydantic class .
        # this is recursive! will call _run() if a given argument value is also a ytBaseModel.
        for arg_i, arg in enumerate(func_spec.args):
            # check if we've remapped the yt internal argument name for the schema
            if arg == 'self':
                continue
            # if arg in self._arg_mapping:
                # arg = self._arg_mapping[arg]

            # get the value for this argument. If it's not there, attempt to set default values
            # for arguments needed for yt but not exposed in our pydantic class
            print("the arguemnt:", arg)
            try:
                arg_value = getattr(self, arg)
                print("the arg value:", arg_value)
                if arg_value == None:
                    default_index = arg_i - named_kw_start_at
                    arg_value = func_spec.defaults[default_index]
                    print('defaults:', default_index, arg_value)
            except AttributeError:
                if arg_i >= named_kw_start_at:
                    # we are in the named keyword arguments, grab the default
                    # the func_spec.defaults tuple 0 index is the first named
                    # argument, so need to offset the arg_i counter
                    default_index = arg_i - named_kw_start_at
                    arg_value = func_spec.defaults[default_index]
                    print('defaults:', default_index, arg_value)
                else:
                    raise AttributeError

            # check if this argument is itself a ytBaseModel for which we need to run
            # this should make this a fully recursive function?
            # if hasattr(arg_value,'_run'):
            if isinstance(arg_value, ytBaseModel) or isinstance(arg_value, ytParameter):
                print(
                    f"{arg_value} is a {type(arg_value)}, calling {arg_value}._run() now...")
                arg_value = arg_value._run()
            # if isinstance(arg_value, ytDataObjectAbstract):
            #     arg_value = arg_value._run(data_source=data_source)

            the_args.append(arg_value)
        print("the args list:", the_args)
        
        # this saves the data from yt.load, so it can be used to instaniate the data object items
        if funcname == 'load':
            self._data_source['test'] = func(*the_args)
        return func(*the_args)

class ytParameter(BaseModel):
    _skip_these = ['comments']

    def _run(self):
        p = [getattr(self, key) for key in self.schema()[
            'properties'].keys() if key not in self._skip_these]
        if len(p) > 1:
            print("some error", p)
            raise ValueError(
                "whoops. ytParameter instances can only have single values")
        return p[0]

class ytDataObjectAbstract(ytBaseModel):
    # abstract class for all the data selectors to inherit from

    def _run(self):
        from yt.data_objects.data_containers import data_object_registry

        the_args = []
        funcname = getattr(self, "_yt_operation", type(self).__name__)
        print("function name:", funcname)

        val = data_object_registry[funcname]
        #func_spec = getfullargspec(val)
        
        # get the function from the data object registry
        val = data_object_registry[funcname]
        print("function:", val)
             
        # iterate through the arguments for the found data object
        for arguments in val._con_args:
            print("the args:", arguments)
            con_value = getattr(self, arguments)
            print(con_value)

            # check that the argument is the correct instance
            if isinstance(con_value, ytDataObjectAbstract):
                # call the _run() function on the agrument
                con_value = con_value._run()
            the_args.append(con_value)
  
        print("the argument list:", the_args)
        # if there is a dataset sitting in _data_source, add it to the args and call as a keyword argument
        if len(self._data_source) > 0:
            ds = list(self._data_source.values())[0]
            return val(*the_args, ds=ds)
        else:
            return val(*the_args)
