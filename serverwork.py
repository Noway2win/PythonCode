from http.server import SimpleHTTPRequestHandler
import Consts
import custom_func
from Consts import project_dir
from errors import NotFound
import traceback
from errors import MethodNotAllowed
from custom_class import Endpoint
from web_app_namespace import Web_App_Names


class MyHandler(SimpleHTTPRequestHandler):
    def respond(self, message, code=200, content_type="text/html", max_age=Consts.CACHE_AGE):
        self.send_response(code)
        self.send_header("Content-Type", content_type)  # вынести контент тайп
        self.send_header("Content-Length", str(len(message)))
        self.send_header("Cache-control", f"public, max-age={max_age}")
        self.end_headers()
        message = custom_func.to_bytes(message)
        self.wfile.write(message)

    def handle_hello(self, endpoint):
        name_dict = Web_App_Names.get_qs_info(endpoint.query_string)
        content = f"""
                <html>
                <head>
                <title>Hello Page</title>
                <link rel="stylesheet" href="/style/hello.css/">
                </head>
                <body>
                <h1 class="ribbon"><strong class="ribbon-content">Hello {name_dict.name} {name_dict.surname}!</strong></h1>
                <h1>{name_dict.year}!</h1>
                <p><a href="/html_files/index.html" class="btn"> Opening_page </a></p>
                </body>
                </html>
                """

        self.respond(content)

    def import_file(self, path, mode="rb", content="image", filetype="jpg"):
        file = project_dir / path
        if not file.exists():
            return self.import_file("html_files/404.html", "r", "text", "html")
        with file.open(mode) as fp:
            file = fp.read()
        self.respond(file, content_type=f"{content}/{filetype}")

    def do_GET(self):
        endpoint = Endpoint.from_path(self.path)
        content_type = custom_func.get_contenttype(endpoint.file_name)
        requests = {
                    "/hello/": [self.handle_hello, [endpoint]],
                    "/style/": [self.import_file, [f"styles/{endpoint.file_name}", "r", "text", "css"]],
                    "/images/": [self.import_file, [f"images/{endpoint.file_name}", "rb", "image", f"{content_type}"]],
                    "/html_files/": [self.import_file, [f"html_files/{endpoint.file_name}", "r", "text", "html"]],
                    }
        try:
            handler, args = requests[endpoint.normal]
            handler(*args)
        except (NotFound, KeyError):
            self.import_file("html_files/404.html", "r", "text", "html")
        except MethodNotAllowed:
            self.respond("", code=405, content_type="text/plain")
        except Exception:
            self.respond(traceback.format_exc(), code=500, content_type="text/plain")
