"""Console script for analysis_schema."""
import sys
import click
import analysis_schema


@click.group()
def main():
    pass


@main.command()
@click.option(
    "--output",
    default=None,
    help="output filename. If not set, print to screen (default)",
)
@click.option(
    "--model_type",
    default="ytModel",
    help="the schema model type (default ytModel)"
)
@click.option(
    "--schema_object",
    default=None,
    help=(
        "a subset of the full schema to generate. "
        "If not set, generate schema for the whole model "
        "(default). Use list_objects to generate list of "
        "valid object names."
    ),
)
def generate(model_type, schema_object, output):
    """ generate a schema file """

    if hasattr(analysis_schema, model_type) is False:
        raise ValueError(f"{model_type} is not a valid analysis_schema model")

    # instantiate an empty model
    emr = analysis_schema.SchemaModel._empty_model_registry
    model_class, model_kwargs = emr[model_type]
    model = model_class(**model_kwargs)

    if schema_object:
        # pull out a subset of the whole schema based on schema_object
        # raise NotImplementedError
        click.echo(f"Generating schema for {schema_object}")
        if hasattr(model, schema_object):
            obj = getattr(model, schema_object)
        else:
            raise ValueError(f"{model_type} does not contain {schema_object}.")
        if type(obj) is list:
            obj = obj[0]
        s = obj.schema_json(indent=2)
    else:
        click.echo(f"Generating schema for {model_type}")
        s = model.schema_json(indent=2)

    if output is None:
        click.echo_via_pager(s)
    else:
        click.echo("Outputting to {}".format(output))
        with open(output, "w") as f:
            f.write(s)


@main.command()
@click.option(
    "--model_type",
    default="ytModel",
    help="the schema model type (default ytModel)"
)
def list_objects(model_type):
    """ list schema_object types for a model type"""
    emr = analysis_schema.SchemaModel._empty_model_registry
    _, model_kwargs = emr[model_type]
    click.echo(f"Available schema_object values for {model_type} include:")
    for name in sorted(model_kwargs.keys()):
        click.echo(f"{name}")


@main.command()
def list_model_types():
    click.echo("Available model types:")
    emr = analysis_schema.SchemaModel._empty_model_registry
    for name in sorted(analysis_schema.SchemaModel._model_types):
        model_class, _ = emr[name]
        click.echo(f"{name} ({model_class})")


server_defaults = analysis_schema.server.server_defaults


@main.command()
@click.option("--host", default=server_defaults["h"], help="Hostname to listen at")
@click.option("--port", default=server_defaults["p"], help="Port to serve on")
def editor(host, port):
    click.echo(f"Launching on {host}:{port}")
    analysis_schema.server.run(host, port, cli=True)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
