import enum
import typing

from pydantic import BaseModel, Schema, create_model

from .fields import FieldName, FieldParameter
from .quantities import (Path, UnitfulArray, UnitfulCoordinate, UnitfulValue,
                         Vector)


class FlatDefinitionsEnum(str, enum.Enum):
    all_data = "all_data"


class BooleanOpEnum(str, enum.Enum):
    AND = "AND"
    OR = "OR"
    XOR = "XOR"
    NOT = "NOT"
    NEG = "NEG"


class BaseDataObject(BaseModel):
    field_parameters: typing.Dict[str, FieldParameter] = {}


class ArbitraryGrid(BaseDataObject):
    _name = "arbitrary_grid"
    left_edge: UnitfulCoordinate
    right_edge: UnitfulCoordinate
    ActiveDimensions: typing.Tuple[int, int, int]


class BooleanContainer(BaseDataObject):
    _name = "bool"
    op: BooleanOpEnum
    obj1: BaseDataObject
    obj2: typing.Union[BaseDataObject, None]


class CoveringGrid(BaseDataObject):
    _name = "covering_grid"
    level: int
    left_edge: UnitfulCoordinate
    ActiveDimensions: typing.Tuple[int, int, int]


class CutRegion(BaseDataObject):
    _name = "cut_region"
    base_object: BaseDataObject
    conditionals: typing.List[str]


class CuttingPlane(BaseDataObject):
    _name = "cutting"
    normal: typing.Tuple[float, float, float]
    center: UnitfulCoordinate


class DataCollection(BaseDataObject):
    _name = "data_collection"
    _obj_list: typing.List[BaseDataObject]


class Disk(BaseDataObject):
    _name = "disk"
    center: UnitfulCoordinate
    _norm_vec: typing.Tuple[float, float, float]
    radius: UnitfulValue
    height: UnitfulValue


class Ellipsoid(BaseDataObject):
    _name = "ellipsoid"
    center: UnitfulCoordinate
    _A: UnitfulValue
    _B: UnitfulValue
    _C: UnitfulValue
    _e0: float
    _tilt: float


class IntersectionContainer3D(BaseDataObject):
    _name = "intersection"
    data_objects: typing.List[BaseDataObject]


class MinimalSphere(BaseDataObject):
    _name = "sphere"
    center: UnitfulCoordinate
    radius: UnitfulValue


class Octree(BaseDataObject):
    _name = "octree"
    left_edge: UnitfulCoordinate
    right_edge: UnitfulCoordinate
    n_ref: int


class OrthoRay(BaseDataObject):
    _name = "ortho_ray"
    axis: typing.Union[str, int]
    coords: typing.Union[UnitfulCoordinate, typing.Tuple[UnitfulValue, UnitfulValue]]


class ParticleProj(BaseDataObject):
    _name = "particle_proj"
    axis: typing.Union[str, int]
    field: FieldName
    weight_field: FieldName


class Point(BaseDataObject):
    _name = "point"
    p: UnitfulCoordinate


class QuadTreeProj(BaseDataObject):
    _name = "quad_proj"
    axis: typing.Union[str, int]
    field: FieldName
    weight_field: FieldName


class Ray(BaseDataObject):
    _name = "ray"
    start_point: UnitfulCoordinate
    end_point: UnitfulCoordinate


class Region(BaseDataObject):
    _name = "region"
    center: UnitfulCoordinate
    left_edge: UnitfulCoordinate
    right_edge: UnitfulCoordinate


class Slice(BaseDataObject):
    _name = "slice"
    axis: typing.Union[str, int]
    coord: typing.Union[UnitfulCoordinate, UnitfulValue]


class SmoothedCoveringGrid(BaseDataObject):
    _name = "smoothed_covering_grid"
    level: int
    left_edge: UnitfulCoordinate
    ActiveDimensions: typing.Tuple[int, int, int]


class Sphere(BaseDataObject):
    _name = "sphere"
    center: UnitfulCoordinate
    radius: UnitfulValue


class Streamline(BaseDataObject):
    _name = "streamline"
    positions: typing.List[UnitfulCoordinate]


class Surface(BaseDataObject):
    _name = "surface"
    data_source: BaseDataObject
    surface_field: FieldName
    field_value: UnitfulValue


class DataObjectUnion(BaseDataObject):
    _name = "union"
    data_objects: typing.List[BaseDataObject]


DataObject = FlatDefinitionsEnum


class AllData(BaseModel):
    all_data: str = "all_data"


for cls in BaseDataObject.__subclasses__():
    if not getattr(cls, "_name", None):
        continue
    name = cls._name
    fields = {name: (cls, ...)}
    locals()[f"{cls.__name__}ID"] = new_model = create_model(
        f"{cls.__name__}ID", **fields
    )
    DataObject = typing.Union[DataObject, new_model]

DataSource = DataObject
