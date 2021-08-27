import time
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple, Union

from pydantic import BaseModel, Schema, create_model

from .data_objects import DataObject
from .dataset import Dataset
from .products import Profile
from .quantities import Path, UnitfulArray, UnitfulCoordinate, UnitfulValue, Vector


class StreamGrid(BaseModel):
    parent_id: int = -1
    Level: int = -1
    children_ids: List[int]
    # this value was hard coded:
    id_offset: int = 0


class StreamHandler(BaseModel):
    # not sure about these:
    num_grids: int
    code_units: str
    processor_ids: list
    io: str
    field_units: str
    parent_ids: str
    particle_types: str
    particle_count: int
    # not sure if this is should be a Vector, or an np.array:
    right_edges: Vector
    periodicity: str
    _fields: list
    # not sure if this is should be a Vector, or an np.array:
    left_edges: Vector
    levels: str
    dimensions: int


class StreamHierarchy(BaseModel):
    dataset_type: str
    # calls previous 'StreamHandler' class attribute
    num_grids: int
    stream_handler: Dataset = StreamHandler
    max_level: int
    # Wasn't sure about this one:
    io: Any
    grid_dimensions: int
    grid_procs: list
    float_type: str = "float64"
    dataset: Dataset = None
    # in file, directory variable calls 'os.getcwd()'
    directory: Any
    grids: list = []
    field_list: list
    # calls previous 'StreamGrid' class
    grid: StreamGrid


class StreamFieldInfo(BaseModel):
    pass


class StreamDataset(BaseModel):
    # astro specific stuff:
    # there's a lot I'm not sure about:
    cosmological_simulation: int = 1
    stream_handler: StreamHandler
    unique_identifer: str = "CurrentTimeIdentifier"
    dimensionality: int
    # really not sure about the astro specific ones
    omega_lambda: int
    omega_matter: str
    fields_units: str
    particle_units: str
    current_redshifts: float
    particle_types_raw: Set[List]
    hubble_constant: float = 0.0
    basename: str
    domain_left_edge: float
    domain_right_edge: float
    periodicity: str
    geometry: str = "cartesian"
    domain_dimensions: int
    current_time: float = time.time()
    gamma: float = 5.0 / 3.0
    # not sure about refine_by
    refine_by: Any
    index_class: StreamHierarchy
    # do we have a type for function calls?
    field_info_class: StreamFieldInfo  # not defined yet, should be defined in fields file
    dataset_type: str = "stream"


class StreamDictFieldHandler(BaseModel):
    additional_fields: Any


class StreamParticleIndex(BaseModel):
    # dataset calls streamhandler, how to type annotation that?
    stream_handler: Dataset
    # I can't tell what the io type would be
    io: Any


class StreamParticleFile(BaseModel):
    pass


class StreamParticleDataset(BaseModel):
    index_class: StreamParticleIndex
    file_class: StreamParticleFile
    field_info_class: StreamFieldInfo  # not defined yet
    dataset_type: str = "stream_particles"
    file_count: int = 1
    filename_template: str = "stream_file"
    n_ref: int = 64
    over_refine_factor: int = 1


class StreamHexahedralMesh(BaseModel):
    connectivity_length: int = 8
    index_offset: int = 0


class StreamHexahedralHiearchy(BaseModel):
    # dataset calls streamhandler, how to type annotation that?
    stream_handler: Dataset
    io: Any
    field_list: List[Set]
    meshes: List[StreamHexahedralMesh]


class StreamHexahedralDataset(BaseModel):
    index_class: StreamHexahedralHiearchy
    field_info_class: StreamFieldInfo  # not yet defined
    dataset_type: str = "stream_hexahedral"


class StreamOctreeSubset(BaseModel):
    field_parameters: Dict = {}
    # what is a base selector
    base_selector: Any
    # YTFieldData() is specific for field_data
    field_data: Any
    oct_handler: Any
    last_mask: Any
    last_selector_id: Any
    current_particle_type: str = "io"
    num_zones: int = 1
    ds: Dataset
    current_fluid_type: str
    base_region: Any
    domain_id: int = 1
    domain_offset: int = 1


class StreamOctreeHandler(BaseModel):
    # maybe str?
    dataset_type: Any = None
    # from stream handler
    stream_handler: Dataset
    io: Any
    # could probably be more specific here
    oct_handler: Dict
    field_list: List[Set]


class StreamOctreeDataset(BaseModel):
    index_class: StreamOctreeHandler
    field_info_class: StreamFieldInfo  # not yet defined
    dataset_type: str = "stream_octree"


class StreamUnstructuredMesh(BaseModel):
    connectivity_length: int
    index_offset: int = 0


class StreamUnstructuredIndex(BaseModel):
    stream_handler: Dataset
    io: Any
    mesh_union: Tuple[str, int]
    field_list: List[Set]
    meshes: List[StreamUnstructuredMesh]


class StreamUnstructuredMeshDataset(BaseModel):
    index_class: StreamUnstructuredIndex
    field_info_class: StreamFieldInfo  # not yet defined
    dataset_type: str = "stream_unstructured"


_field_name = Union[Tuple[str, str], str]
_field_values = Union[Any, Tuple[Any, str]]


class AMRGridDataSpecification(BaseModel):
    # Maps to a single element of the `grid_data` argument to yt.load_amr_grids
    # Note that the "fields" here are what would normally be in the rest of the dict
    left_edge: Tuple[float, float, float]
    right_edge: Tuple[float, float, float]
    dimensions: Tuple[int, int, int]
    level: int
    field_data: Dict[_field_name, _field_values]


class AMRDataSpecification(BaseModel):
    # load_amr_grids
    grid_data: List[AMRGridDataSpecification] = None
    domain_dimensions: Tuple[int, int, int] = None
    length_unit: Union[str, float] = None
    mass_unit: Union[str, float] = None
    time_unit: Union[str, float] = None
    velocity_unit: Union[str, float] = None
    magnetic_unit: Union[str, float] = None
    bbox: Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]] = None
    sim_time: float = 0.0
    periodicity: Tuple[bool, bool, bool] = (True, True, True)
    geometry: Union[str, Tuple[str, Tuple[str, str, str]]] = "cartesian"
    refine_by: Union[List[int], int] = 2


class YTDatasetSpecification(BaseModel):
    data_specification: Union[AMRDataSpecification] = None
