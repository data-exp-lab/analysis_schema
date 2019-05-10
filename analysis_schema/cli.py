# -*- coding: utf-8 -*-

"""Console script for analysis_schema."""
import sys
import click
import http.server

@click.group()
def main():
    pass

@main.command()
@click.argument("name")
@click.option("--output", default=None, help='output filename')
def generate(name, output):
    click.echo("Hi there!  Generating {}.".format(name))
    if output is None:
        click.echo("No output")
    else:
        click.echo("Outputting to {}".format(output))

@main.command()
@click.argument("editor")
@click.option("--port", default=8000, help='Port to serve on')
def editor(port):
    # TODO: Make this work with the generated files
    http.server.SimpleHTTPServer()

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
