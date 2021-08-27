#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system("pip install pydantic")


# In[2]:


get_ipython().system(" pip install pydantic[ujson]")


# In[3]:


get_ipython().system(" pip install pydantic[email]")


# In[15]:


import pydantic
import yt

# In[4]:




# In[5]:


print("compiled", pydantic.compiled)


# In[6]:


from datetime import datetime
from typing import List

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name = "John Doe"
    signup_ts: datetime = None
    friends: List[int] = []


external_data = {
    "id": "123",
    "signup_ts": "2017-06-01 12:22",
    "friends": [1, "2", b"3"],
}
user = User(**external_data)
print(user)

print(user.id)


# Does each frontend became a class and/or methods?

# In[11]:


## try some yt like stuff
## create schema


class domain(BaseModel):
    file_name: str = None
    frontend: str = None


test_data = {"frontend": "neuro", "file_name": "nii.gz"}
dd = domain(**test_data)

print(dd)
print(dd.file_name)


# In[14]:


get_ipython().system("pwd")


# In[53]:


## try HDF5 scheme


class Dataset:
    def __init__(self, fid, shape: int, header: str):
        self.fid: str = fid
        self.shape: int
        self.header: str


test = Dataset(fid="test.txt", shape=3, header="test")
print(test.fid)


# In[62]:


class datatypes(BaseModel):
    fid: str
    shape: List[int]


d = {"fid": "testing", "shape": [3, 3, 4]}
hd = datatypes(**d)
print(hd)


# In[68]:


class MainModel(pydantic.BaseModel):
    data: datatypes = pydantic.Schema("test.txt", shape=[3, 2, 4])

    class Config:
        title = "New Schema"


# In[69]:


print(MainModel.schema())


# In[70]:


print(MainModel.schema_json(indent=2))


# use enzo data - enzo heichary .heichary, skip the pointers (make everything typed)

# pull up the "invalidators" and put in schema

# Do all type annotations

# In[157]:


get_ipython().run_line_magic("pinfo", "pydantic.BaseModel")


# In[175]:


# building a schema for enzo hierarchy


class EnzoGrid(BaseModel):
    Grid: int
    Task: int = 0
    GridRank: int
    GridDimension: List[int]
    GridStartIndex: List[int]
    GridEndIndex: List[int]
    GridLeftEdge: List[int] = [0, 0]
    GridRightEdge: List[int] = [1, 1]
    Time: int = 1
    SubGridsAreStatic: int
    NumberOfBaryonFields: int
    FieldType: List[int]
    BaryonFileName: str
    CourantSafetyNumber: float
    PPMFlatteningParameter: int
    PPMDiffusionParameter: int
    PPMSteepeningParameter: int
    NumberOfParticles: int


# In[191]:


# storing values in a variable, that are then passed into a the enzo schema

e = {
    "Grid": 1,
    "Task": 0,
    "GridRank": 3,
    "GridDimension": [70, 70],
    "GridStartIndex": [3, 3],
    "GridEndIndex": [66, 66],
    "SubGridsAreStatic": 0,
    "NumberOfBaryonFields": 4,
    "FieldType": [0, 1, 4, 5],
    "BaryonFileName": "./DD0011/DD0011.cpu0000",
    "CourantSafetyNumber": 0.400000,
    "PPMFlatteningParameter": 0,
    "PPMDiffusionParameter": 0,
    "PPMSteepeningParameter": 0,
    "NumberOfParticles": 0,
}
eg = EnzoGrid(**e)
print(eg)


# In[192]:


# defining the enzo model
# how to best use the model? What else needs to be added?


class EnzoModel(BaseModel):
    hierarchy: EnzoGrid = pydantic.Schema(..., **e)

    class Config:
        title = "Enzo Schema"


# In[193]:


print(EnzoModel.schema())


# In[194]:


print(EnzoModel.schema_json(indent=2))


# In[207]:


ds = yt.load("/Users/swalkow2/Downloads/Data/EnzoKelvinHelmholtz/DD0011/DD0011")


# In[211]:


print(ds.domain_dimensions)


# In[212]:


print(ds.field_list)


# In[214]:


ds.get_metadata()


# In[213]:


deg = enzo_grid(**ds)
print(deg)


# In[250]:


text = open(
    "/Users/swalkow2/Downloads/Data/EnzoKelvinHelmholtz/DD0011/DD0011.hierarchy", "r"
)


# In[251]:


reading = text.readlines()


# In[253]:


for r in reading:
    print(r)


# In[ ]:
