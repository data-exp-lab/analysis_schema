# -*- coding: utf-8 -*-

"""Console script for analysis_schema."""
import sys
import click
# import http.server
from .SchemaModel import schema
from .server import run as run_editor, server_defaults


@click.group()
def main():
    pass


@main.command()
@click.option("--output", default=None, help="output filename")
@click.argument("schema_object", default="Operation")
def generate(schema_object, output):
    click.echo("Generating schema for Operation")
    obj = schema["properties"][schema_object]  # TODO: add error
    s = obj.schema_json(indent=2)
    if output is None:
        click.echo_via_pager(s)
    else:
        click.echo("Outputting to {}".format(output))
        with open(output, "w") as f:
            f.write(s)


@main.command()
def list_objects():
    for name in sorted(schema):
        click.echo("Object available: {}".format(name))



@main.command()
@click.option("--host", default=server_defaults["h"], help="Hostname to listen at")
@click.option("--port", default=server_defaults["p"], help="Port to serve on")
def editor(host, port):
    click.echo(f"Launching on {host}:{port}")
    run_editor(host, port, cli=True)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
