# -*- coding: utf-8 -*-

"""Console script for analysis_schema."""
import sys
import click
import http.server
from operations import Operation
from server import run as run_editor

@click.group()
def main():
    pass

@main.command()
@click.option("--output", default=None, help='output filename')
def generate(output):
    click.echo("Generating schema for Operation")
    s = Operation.schema_json(indent = 2)
    if output is None:
        click.echo_via_pager(s)
    else:
        click.echo("Outputting to {}".format(output))
        with open(output, "w") as f:
            f.write(s)

@main.command()
@click.option("--host", default="localhost", help="Hostname to listen at")
@click.option("--port", default=8000, help='Port to serve on')
def editor(host, port):
	run_editor(host, port)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
