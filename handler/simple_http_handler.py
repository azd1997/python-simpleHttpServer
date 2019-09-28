import os
import json
from handler.base_http_handler import BaseHTTPRequestHandler
from urllib import parse

# 获取当前文件夹目录并转换为绝对路径，再与'../resources'合并，就得到了resources路径
RESOURCES_PATH = os.path.join(os.path.abspath(os.path.dirname(__name__)), '../resources')


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, server, request, client_address):
        BaseHTTPRequestHandler.__init__(self, server, request, client_address)

    def do_GET(self):
        found, resource_path = self.get_resources(self.path)
        if not found:
            self.write_error(404)
            self.send()
        else:
            with open(resource_path, 'rb') as f:
                # 调用系统API获取文件内容长度，在fs的第7个位置
                fs = os.fstat(f.fileno())
                clength = str(fs[6])
                self.write_response(200)
                self.write_header('Content-Length', clength)
                self.end_headers()
                while True:
                    buf = f.read(1024)
                    if not buf:
                        break
                    self.write_content(buf)
                # 不需要self.send()。因为handle中下一步就是send
        pass

    # 判断路径并获取资源
    def get_resources(self, path):
        url_result = parse.urlparse(path)
        resource_path = str(url_result[2])
        if resource_path.startswith('/'):
            resource_path = resource_path[1:]
        resource_path = os.path.join(RESOURCES_PATH, resource_path)
        if os.path.exists(resource_path) and os.path.isfile(resource_path):
            return True, resource_path
        else:
            return False, resource_path

    def do_POST(self):
        # 账号密码的校验
        body = json.loads(self.body)
        username = body['username']
        password = body['password']
        if username == 'eiger' and password == '123456':
            response = {'message': 'success', 'code': 0}
        else:
            response = {'message': 'failed', 'code': -1}
        response = json.dumps(response)
        self.write_response(200)
        self.write_header('Content-Length', len(response))
        # 避免跨域问题
        self.write_header('Access-Control-Allow-Origin', 'http://%s:%d' % (self.server.server_address[0], self.server.server_address[1]))
        self.end_headers()
        self.write_content(response)