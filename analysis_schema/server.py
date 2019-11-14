from .operations import Operation
from .analysis_schema import schema
import http.server
import pkg_resources

# For static serving:
# _index_contents = pkg_resources.resource_string(__name__, "index.html")

# Implement do_GET for only the files we want -- index.html and the schema

_monaco_env = b"""
self.MonacoEnvironment = {
    baseUrl: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.17.0/min/'
};
importScripts('https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.17.0/min/vs/base/worker/workerMain.js');
"""


class EditorHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            return self.return_index()
        elif self.path == "/schema.json":
            return self.return_schema()
        elif self.path == "/monaco-editor-worker-loader-proxy.js":
            return self.return_worker_proxy()
        self.send_response(404)

    def return_index(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        _index_contents = pkg_resources.resource_string(__name__, "index.html")
        self.wfile.write(_index_contents)
        return

    def return_schema(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(self.server._schema_definition.encode("utf-8"))
        return

    def return_worker_proxy(self):
        self.send_response(200)
        self.send_header("Content-type", "application/javascript")
        self.end_headers()
        self.wfile.write(_monaco_env)
        return


class SchemaHTTPServer(http.server.HTTPServer):
    def __init__(self, *args, schema_object="Operation", **kwargs):
        obj = schema[schema_object]  # TODO: add error
        self._schema_definition = obj.schema_json(indent=2)
        super().__init__(*args, **kwargs)


def run(host, port, schema_object="Operation"):
    server_address = (host, port)
    httpd = SchemaHTTPServer(server_address, EditorHandler, schema_object=schema_object)
    httpd.serve_forever()
