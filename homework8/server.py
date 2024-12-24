from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import os
from requests import get, put
import urllib.parse
import json
import sys

class Handler(BaseHTTPRequestHandler):
    def __init__(self, auth_key, *args):
        self.html_template = """
        <html>
            <head>
                <style>
                    li.uploaded {{background-color:rgba(0, 200, 0, 0.25)}}
                    li.normal {{}}
                </style>
            </head>
            <body>
                <ul>
                {files}
                </ul>
            </body>
        </html>
        """
        self.item_format = """
        <li class="{style}", onclick="fetch('/upload',{{'method': 'POST', 'body': '{name}'}})">
            {name}
        </li>"""
        self.uploaded_files = set()
        self.disk_url = "https://cloud-api.yandex.net/v1/disk/resources?path={path}&fields=_embedded.items.name,_embedded.limit&sort=name&offset={offset}"
        self.upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload?path={path}"
        self.disk_folder = "Backup"
        self.disk_auth_header = {"Authorization": f"OAuth {auth_key}"}
        BaseHTTPRequestHandler.__init__(self, *args)

    def get_file_list_chunk(self, offset):
        response = get(self.disk_url.format(path=self.disk_folder, offset=offset),headers=self.disk_auth_header)
        if len(response.text) == "":
            return (True, 0)
        files = json.loads(response.text)
        for file in files["_embedded"]["items"]:
            self.uploaded_files.add(file["name"])
        limit = int(files["_embedded"]["limit"])
        return (len(files["_embedded"]["items"]) < limit, limit)

    def get_file_list(self):
        self.uploaded_files = set()
        offset = 0
        result = self.get_file_list_chunk(offset)
        while not result[0]:
            offset += result[1]
            result = self.get_file_list_chunk(offset)

    def get_item(self, file_name):
        print(file_name)
        if file_name in self.uploaded_files:
            return self.item_format.format(style='uploaded', name=file_name)
        else:
            return self.item_format.format(style='normal', name=file_name)

    def do_GET(self):
        #По аналогии с кодом с вебинара
        self.get_file_list()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(self.html_template.format(files='\n'.join(map(self.get_item, os.listdir("pdfs")))).encode())

    def do_POST(self):
        #Взято с изменениями из кода с вебинара (в тексте ДЗ указано взять его за основу)
        content_len = int(self.headers.get('Content-Length'))
        fname = self.rfile.read(content_len).decode("utf-8")
        local_path = f"pdfs/{fname}"
        ya_path = f"{self.disk_folder}/{urllib.parse.quote(fname)}"
        resp = get(self.upload_url.format(path=ya_path),headers=self.disk_auth_header)
        upload_url = json.loads(resp.text)["href"]
        resp = put(upload_url, files={'file': (fname, open(local_path, 'rb'))})
        self.send_response(200)
        self.end_headers()

def run():
    auth_key = input('Enter Yandex Disk auth key:\n')
    def make_handler(*args):
        return Handler(auth_key, *args)
    httpd = HTTPServer(('', 8080), make_handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()

run()

