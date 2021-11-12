#from __future__ import annotations
import pydantic
from typing import get_type_hints, Dict, List
import pandas as pd
from pandas.core.internals import SingleBlockManager
from pandas.core.indexes.base import Index
from collections import Counter
import numpy as np
from pydantic import BaseModel
from BaseModelFunctions import ytBaseModel

array = np.arange(1,10)
data_dict = {'col1': [1, 2], 'col2': [3, 4]}
#
# qhelp(pd.DataFrame)
#print(get_type_hints(np.where()))

# df = pd.DataFrame(data=data_dict)
# ser = pd.Series(data=data_dict, index=["col1", "col2"])

# # Trying to get annotations
# print(pd.DataFrame.__annotations__)
# # print()
# get_type_hints(pd.DataFrame, localns={'SingleBlockManager': SingleBlockManager})

# # Once I have annotations, can I create a model using a loop?

class DataFrameAuto():
    _yt_operation = "DataFrame"
    data: Dict = None

    def adding_new_attr(self, attr):
        setattr(self, attr, attr)

    def _run(self):
         # for the top level model, we override this.
        # Nested objects will still be recursive!
        output_list = []
        for attribute in dir(self):
            if not attribute.startswith('_'):
                print(attribute)


df = DataFrameAuto()

for attr, anno in pd.DataFrame.__annotations__.items():
    if not attr[0].startswith('_'):
        print(attr)
        print(locals()[anno.capitalize()])
        local = locals()[anno.capitalize()]
        # if anno.capitalize() in locals().keys():
        #     #print("locals", anno, locals().keys())
        setattr(df, attr, local)

# print(dir(df))
# print(df.index)
# print(df.columns)
# print(df.data)
#print(locals().items())

# schema = DataFrameAuto
# schema_dict = schema.schema()
# print(schema.schema_json(indent=2))


# # Can I create a model (not automated) using `BaseModel` and dataframe as a type for an attribute
# class df_model(pydantic.BaseModel):
#     dataframe: pd.DataFrame 

#     class Config:
#         arbitrary_types_allowed = True

# print(df_model.schema_json(indent=2))

class DataFrame(ytBaseModel):
    data: Dict
    index: List
    columns: List
    _yt_operation = "DataFrame"

    class Config:
        title = "DataFrame Schema Model - Test"
        underscore_attrs_are_private = True

    def _run(self):
        # for the top level model, we override this.
        # Nested objects will still be recursive!
        output_list = []
        for attribute in dir(self):
            if not attribute.startswith('_'):
                print(attribute)

# schema = DataFrame
# schema_dict = schema.schema()
# print(schema.schema_json(indent=2))