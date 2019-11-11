from pydantic import BaseModel, Schema, create_model
from typing import Dict, List, Optional, Sequence, Set, Tuple, OrderedDict, Any
import enum

from .quantities import UnitfulCoordinate, Vector, Path, UnitfulValue, UnitfulArray
from .data_objects import DataObject
from .dataset import Dataset
from .products import Profile

class StreamGrid(BaseModel):
    parent_id : int = 1
    Level : int = -1
    children_ids : list
    # this value was hard coded:
    slots : list = ['proc_num']
    id_offset : int = 0

class StreamHandler(BaseModel):
    # not sure about these:
    num_grids : int
    code_units : str
    processor_ids : list
    io : str
    field_units : str
    parent_ids : str
    particle_types : str
    particle_count : int
    # not sure if this is should be a Vector, or an np.array:
    right_edges : Vector
    periodicity : str
    fields : list
    # not sure if this is should be a Vector, or an np.array:
    left_edges : Vector
    levels : str
    dimensions : int

class StreamHierarchy(BaseModel):
    dataset_type : str
    # calls previous 'StreamHandler' class attribute
    num_grids : int
    stream_handler : Dataset = StreamHandler
    max_level : int
    # Wasn't sure about this one:
    io : Any
    grid_dimensions : int
    grid_procs : list
    float_type : str = 'float64'
    dataset : Dataset = None
    # in file, directory variable calls 'os.getcwd()'
    directory : Any
    grids : list = []
    field_list : list
    # calls previous 'StreamGrid' class
    grid : StreamGrid

class StreamDataset(BaseModel):
    # astro specific stuff:
    # there's a lot I'm not sure about:
    cosmological_simulation:
    stream_handler : StreamHandler
    unique_identifer :
    dimensionality :
    omega_lambda :
    omega_matter :
    fields_units :
    particle_units :
    current_redshifts:
    particle_types_raw:
    hubble_constant :
    basename :
    domain_left_edge:
    domain_right_edge :
    periodicity :
    geometry : str = 'cartesian'
    domain_dimensions :
    current_time :
    gamma : float = 5./3.
    refine_by :
    index_class : StreamHierarchy
    field_info_class : StreamFieldInfo # not defined yet, should be defined in fields file
    dataset_type : str = 'stream'

class StreamDictFieldHandler(BaseModel):

class StreamParticleIndex(BaseModel):

class StreamParticleFile(BaseModel):

class StreamParticleDataset(BaseModel):

class StreamHexahedraMesh(BaseModel):

class StreamHexahedraHiearchy(BaseModel):

class StreamHexahedralDataset(BaseModel):

class StreamOctreeSubset(BaseModel):

class StreamOctreeHandler(BaseModel):

class StreamOctreeDataset(BaseModel):

class StreamUnstructuredMesh(BaseModel):

class StreamUnstructuredIndex(BaseModel):

class StreamUnstructuredMeshDataset(BaseModel):


