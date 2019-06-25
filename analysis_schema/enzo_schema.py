#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install pydantic')


# In[2]:


get_ipython().system(' pip install pydantic[ujson]')


# In[3]:


get_ipython().system(' pip install pydantic[email]')


# In[15]:


import yt


# In[4]:


import pydantic


# In[5]:


print("compiled", pydantic.compiled)


# In[6]:


from datetime import datetime
from typing import List
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name = 'John Doe'
    signup_ts: datetime = None
    friends: List[int] = []

external_data = {'id': '123', 'signup_ts': '2017-06-01 12:22', 'friends': [1, '2', b'3']}
user = User(**external_data)
print(user)

print(user.id)


# Does each frontend became a class and/or methods? 

# In[11]:


## try some yt like stuff
## create schema

class domain(BaseModel):
    file_name: str = None
    frontend : str = None
        

test_data = {'frontend':'neuro', 'file_name':'nii.gz'}
dd = domain(**test_data)

print(dd)
print(dd.file_name)


# In[14]:


get_ipython().system('pwd')


# In[53]:


## try HDF5 scheme

class Dataset:
    def __init__(self, fid, shape:int, header: str):
        self.fid : str = fid
        self.shape : int
        self.header : str
    
test = Dataset(fid = 'test.txt', shape = 3, header = 'test')
print(test.fid)


# In[62]:


class datatypes(BaseModel):
    fid : str
    shape : List[int]
        
d = {'fid':'testing', 'shape':[3,3,4]}
hd = datatypes(**d)
print(hd)


# In[68]:


class MainModel(pydantic.BaseModel):
    data : datatypes = pydantic.Schema('test.txt', shape = [3,2,4])
    class Config:
        title = 'New Schema'
    


# In[69]:


print(MainModel.schema())


# In[70]:


print(MainModel.schema_json(indent=2))


# use enzo data - enzo heichary .heichary, skip the pointers (make everything typed)

# pull up the "invalidators" and put in schema

# Do all type annotations

# In[157]:


get_ipython().run_line_magic('pinfo', 'pydantic.BaseModel')


# In[162]:


# building a schema for enzo hierarchy

class EnzoGrid(BaseModel):
    grid : int
    task: int = 0
    grid_rank : int
    grid_dimension : List[int]
    grid_start_index : List[int]
    grid_end_index : List[int]
    grid_left_edge : List[int] = [0,0]
    grid_right_edge : List[int] = [1,1]
    time : int = 1


# In[167]:


# storing values in a variable, that are then passed into a the enzo schema

e = {'grid':1, 'grid_rank': 2, 'grid_dimension': [70,70],
    'grid_start_index': [3,3], 'grid_end_index': [66,66]}
eg = EnzoGrid(**e)
print(eg)


# In[132]:


get_ipython().run_line_magic('pinfo', 'pydantic.Schema')


# In[169]:


# defining the enzo model
# how to best use the model? What else needs to be added?

class EnzoModel(BaseModel):
    hierarchy : EnzoGrid = pydantic.Schema(..., **e)
    class Config:
        title = 'Enzo Schema'


# In[170]:


print(EnzoModel.schema())


# In[171]:


print(EnzoModel.schema_json(indent=2))


# In[147]:


ds = yt.load("/Users/swalkow2/Downloads/Data/EnzoKelvinHelmholtz/DD0011/DD0011.hierarchy")


# In[160]:


print(ds.dimensionality)


# In[156]:


deg = enzo_grid(ds)
print(deg)


# In[ ]:




