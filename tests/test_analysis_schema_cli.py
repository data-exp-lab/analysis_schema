#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `analysis_schema` command line interface."""

import json
import os

from click.testing import CliRunner

from analysis_schema import cli, schema_model


def test_command_line_interface():
    """Test the cli basic invocation"""

    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output


def test_schema_generation(tmpdir):
    """Test schema generation from cli"""

    runner = CliRunner()
    # check the help message
    schema_result = runner.invoke(cli.main, ["generate", "--help"])
    assert schema_result.exit_code == 0
    assert "generate a schema file" in schema_result.output
    assert all(
        [
            s in schema_result.output
            for s in ["--output", "--model_type", "--schema_object"]
        ]
    )

    # check schema-string to screen
    schema_result = runner.invoke(cli.main, ["generate"])
    assert schema_result.exit_code == 0
    mod = schema_model.ytModel()
    s = mod.schema_json(indent=2)
    assert s in schema_result.output

    # check schema file-write
    schema_file = tmpdir.mkdir("schema").join("schema_test.json")
    run_args = ["generate", "--output", schema_file]
    schema_result = runner.invoke(cli.main, run_args)
    assert schema_result.exit_code == 0
    assert os.path.isfile(schema_file)  # read it back in and check it
    with open(schema_file, "r") as sch_fi:
        schema_from_file = json.loads(sch_fi.read())
    assert type(schema_from_file) == dict
    schema = mod.schema()
    assert all([s in schema_from_file.keys() for s in schema.keys()])

    # check that we can generate a schema for a subset of the full schema
    for mtype in schema_model._model_types:
        cls, kwargs = schema_model._empty_model_registry[mtype]
        mod = cls(**kwargs)
        base_args = ["generate", "--model_type", mtype]
        for obj in list(kwargs.keys()):
            run_args = base_args + ["--schema_object", obj]
            schema_result = runner.invoke(cli.main, run_args)
            assert schema_result.exit_code == 0
            submodel = getattr(mod, obj)
            if type(submodel) is not list:
                submodel = [submodel]
            outjson = schema_result.output
            assert all([sm.schema_json(indent=2) in outjson for sm in submodel])

    # check for some errors
    schema_result = runner.invoke(
        cli.main, ["generate", "--model_type", "missing_model"]
    )
    assert schema_result.exit_code == 1
    type(schema_result.exception) == ValueError


def test_schema_availability():
    """check cli methods for printing available models and schema objects"""

    runner = CliRunner()

    # test the model type list generation
    schema_result = runner.invoke(cli.main, ["list-model-types"])
    assert schema_result.exit_code == 0
    assert all([s in schema_result.output for s in schema_model._model_types])

    # or each model type, check the list of schema_objects
    for mtype in schema_model._model_types:
        _, kwargs = schema_model._empty_model_registry["ytModel"]
        run_args = ["list-objects", "--model_type", mtype]
        schema_result = runner.invoke(cli.main, run_args)
        assert schema_result.exit_code == 0
        assert all([s in schema_result.output for s in kwargs.keys()])


def test_run_analysis(tmpdir):

    input_fi = tmpdir / "input.json"
    # this will only instantiate a data_store, not actually load data, so
    # it will run even if the data is not available.
    test_json = {
        "Data": [
            {"FileName": "IsolatedGalaxy/galaxy0030/galaxy0030", "DatasetName": "IG"}
        ]
    }
    with open(input_fi, "w") as input_file:
        input_file.write(json.dumps(test_json))

    runner = CliRunner()
    schema_result = runner.invoke(cli.main, ["run-analysis", str(input_fi)])
    assert schema_result.exit_code == 0
