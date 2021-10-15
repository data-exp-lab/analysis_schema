from __future__ import annotations
import pydantic
import typing
from pandas import DataFrame, Series
from pandas import _typing



data_dict = {'col1': [1, 2], 'col2': [3, 4]}
df = DataFrame(data=data_dict)
# print(df)
# print()
ser = Series(data=data_dict, index=["col1", "col2"])
# print(ser)

# print(DataFrame.__annotations__)
# # print(Series.__annotations__)
# print()
# print(typing.get_type_hints((DataFrame)))
# print()

for attr, anno in DataFrame.__annotations__.items():
    #print(attr, anno)
    model_args = dict()
    if not attr[0].startswith('_'):
        
        model_args[attr] = anno
        df_class = pydantic.create_model("A DataFrame", attr=(anno))

class df_model(pydantic.BaseModel):
    dataframe: DataFrame 

    class Config:
        arbitrary_types_allowed = True

print(df_model.schema_json(indent=2))
#print(dir(_typing))

#print(help(DataFrame))