# -*- coding: utf-8 -*-

"""Console script for analysis_schema."""
import sys
import click
import http.server
from .analysis_schema import schema
from .server import run as run_editor


@click.group()
def main():
    pass


@main.command()
@click.option("--output", default=None, help="output filename")
@click.argument("schema_object", default="Operation")
def generate(schema_object, output):
    click.echo("Generating schema for Operation")
    obj = schema[schema_object]  # TODO: add error
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
@click.option("--host", default="localhost", help="Hostname to listen at")
@click.option("--port", default=8000, help="Port to serve on")
@click.argument("schema_object", default="Operation")
def editor(host, port, schema_object):
    click.echo(f"Launching on {host}:{port}")
    run_editor(host, port, schema_object)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
