from __future__ import annotations
import pydantic
import typing
from pandas import DataFrame, Series
from pandas import _typing



data_dict = {'col1': [1, 2], 'col2': [3, 4]}
df = DataFrame(data=data_dict)
ser = Series(data=data_dict, index=["col1", "col2"])

# Trying to get annotations
print(DataFrame.__annotations__)
print()
print(typing.get_type_hints((DataFrame)))

# Once I have annotations, can I create a model using a loop?
for attr, anno in DataFrame.__annotations__.items():
    if not attr[0].startswith('_'):
        df_class = pydantic.create_model("A DataFrame", attr=(anno))


# Can I create a model (not automated) using `BaseModel` and dataframe as a type for an attribute
class df_model(pydantic.BaseModel):
    dataframe: DataFrame 

    class Config:
        arbitrary_types_allowed = True

print(df_model.schema_json(indent=2))
