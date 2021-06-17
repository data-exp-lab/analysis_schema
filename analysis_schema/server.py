# from .operations import Operation
from .SchemaModel import schema
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
            # can call the default schema through `return_schema`or a different schema from a local JSON file through `return_external_schema`
            return self.return_external_schema()
        elif self.path == "/monaco-editor-worker-loader-proxy.js":
            print("getting worker proxy")
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
        """This function returns the schema generate within this module, which I am calling the defalut schema.
        """
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(self.server._schema_definition.encode("utf-8"))
        return

    def return_external_schema(self):
        """This function grabs a local schema file instead of generating the default schema. To change the file, change file name in `_json_contents` agruements. To change back to the default schema, change the call in `do_GET` under self.path to call return_schema.  
        """
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        # grabs the local file
        _json_contents = pkg_resources.resource_string(__name__, "pydantic_schema.json")
        self.wfile.write(_json_contents)
        return

    def return_worker_proxy(self):
        self.send_response(200)
        self.send_header("Content-type", "application/javascript")
        self.end_headers()
        self.wfile.write(_monaco_env)
        return


class SchemaHTTPServer(http.server.HTTPServer):
    def __init__(self, *args, **kwargs):        
        self._schema_definition = schema.schema_json(indent=2)
        super().__init__(*args, **kwargs)


def run(host = server_defaults["h"], port = server_defaults["p"], cli=False):
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
        print(f"crtl-c to kill server")
    httpd = SchemaHTTPServer(server_address, EditorHandler)
    httpd.serve_forever()
