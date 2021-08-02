""" some tests for the SchemaModel """
from analysis_schema.SchemaModel import _model_types, _empty_model_registry
from pydantic import BaseModel

def test_instantiation():
    """ checks that all the model types can be instantiated """
    for model_type in _model_types:
        cls, kwargs = _empty_model_registry[model_type]
        model = cls(**kwargs)
        assert isinstance(model, BaseModel)


def test_schema_generation():
    """ checks that a json can be generated from each model type """
    for model_type in _model_types:
        cls, kwargs = _empty_model_registry[model_type]
        model = cls(**kwargs)
        model_json = model.schema()
        assert isinstance(model_json, dict)
