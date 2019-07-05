import typing
import enum
from pydantic import BaseModel, Schema, create_model
from .quantities import UnitfulCoordinate, UnitfulValue, UnitfulArray

class DomainContext(BaseModel):
    field_plugins: typing.List[str] = []
    unit_system = str

class CosmologyContext(DomainContext):
    cosmology: bool
    omega_lambda: float
    omega_matter: float
    omega_radiation: float
    hubble_constant: UnitfulValue # maybe just float
    current_redshift: float
    field_aliases: typing.List[typing.Tuple[str, str]]

class TurbulentContext(DomainContext):
    density_power_spectral_index: float
    velocity_power_spectral_index: float
    driven: bool

class NeuroImagingContext(DomainContext):
    registered: bool
    affine_transformation: typing.List[float]

domain_contexts = typing.Union[CosmologyContext,
                               TurbulentContext,
                               NeuroImagingContext]

class Dataset(BaseModel):
    domain_left_edge: UnitfulCoordinate
    domain_right_edge: UnitfulCoordinate
    domain_dimensions: typing.List[float]
    current_time: UnitfulValue
    geometry: str
    dataset_type: str
    domain_contexts: typing.List[domain_contexts]
