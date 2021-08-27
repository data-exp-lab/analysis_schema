import http.server
import traceback
from cgi import parse_header, parse_multipart
from urllib.parse import parse_qs

import pkg_resources

from .SchemaModel import schema

# For static serving:
# _index_contents = pkg_resources.resource_string(__name__, "index.html")

# Implement do_GET for only the files we want -- index.html and the schema

_monaco_env = b"""
self.MonacoEnvironment = {
    baseUrl: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.17.0/min/'
};
importScripts('https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.17.0/min/vs/base/worker/workerMain.js');
"""

server_defaults = {"h": "localhost", "p": 8000, "schema_obj": "Plot"}


class EditorHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            print("returning index")
            return self.return_index()
        elif self.path == "/schema.json":
            # calls a specific schema
            # can call the default schema through `return_schema`
            # or a different schema from a local JSON file through
            # `return_external_schema`
            return self.return_external_schema()
        elif self.path == "/monaco-editor-worker-loader-proxy.js":
            print("getting worker proxy")
            return self.return_worker_proxy()
        self.send_response(404)

    def parse_POST(self):
        ctype, pdict = parse_header(self.headers["content-type"])
        if ctype == "multipart/form-data":
            postvars = parse_multipart(self.rfile, pdict)
        elif ctype == "application/x-www-form-urlencoded":
            length = int(self.headers["content-length"])
            postvars = parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}
        return postvars

    def do_POST(self):
        if "/run_schema" in self.path:
            postvars = self.parse_POST()
            print("running schema")
            return self.run_schema(postvars)

    def return_index(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        _index_contents = pkg_resources.resource_string(__name__, "index.html")
        self.wfile.write(_index_contents)
        return

    def return_schema(self):
        """
        This function returns the schema generate within this module,
        which I am calling the defalut schema.
        """
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(self.server._schema_definition.encode("utf-8"))
        return

    def return_external_schema(self):
        """
        This function grabs a local schema file instead of generating
        the default schema. To change the file, change file name in
        `_json_contents` agruements. To change back to the default schema,
        change the call in `do_GET` under self.path to call return_schema.
        """
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        # grabs the local file
        _json_contents = pkg_resources.resource_string(
            __name__, "yt_analysis_schema.json"
        )
        self.wfile.write(_json_contents)
        return

    def return_worker_proxy(self):
        self.send_response(200)
        self.send_header("Content-type", "application/javascript")
        self.end_headers()
        self.wfile.write(_monaco_env)
        return

    def run_schema(self, postvars: dict):
        # the validated json is an argument in the path

        json_str = postvars[b"json"][0].decode()
        yt_results = run_a_schema(json_str)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        _index_contents = '<div id="results">' + yt_results + "</div>"

        self.wfile.write(_index_contents.encode())


class SchemaHTTPServer(http.server.HTTPServer):
    def __init__(self, *args, **kwargs):
        self._schema_definition = schema.schema_json(indent=2)
        super().__init__(*args, **kwargs)


def run(host=server_defaults["h"], port=server_defaults["p"], cli=False):
    """
    run from command line using cli (see docstring in cli.py) or run from
    interactive shell with

    >>> from analysis_schema import server
    >>> server.run()
    """

    server_address = (host, port)
    if cli is False:
        print(f"starting server at {host}:{port}")
        print(f"visit http://{host}:{port} to launch schema editor")
        print("crtl-c to kill server")
    httpd = SchemaHTTPServer(server_address, EditorHandler)
    httpd.serve_forever()


def run_a_schema(json_payload_str):

    # parse and validate
    try:
        valid_json = schema.parse_raw(json_payload_str)
    except Exception as ex:
        return "".join(
            traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        )

    # run it
    try:
        results = valid_json._run()
    except Exception as ex:
        return "".join(
            traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)
        )

    # convert results
    html_results = []
    for result in results:
        if hasattr(result, "_repr_html_"):
            html_results.append(result._repr_html_())
        else:
            html_results.append("<div> object does not have a _repr_html </div>")
    return "".join(html_results)
