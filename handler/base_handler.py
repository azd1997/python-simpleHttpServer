# -*- encoding=utf-8 -*-


class BaseRequestHandler:
    def __init__(self, server, request, client_address):
        self.server = server
        self.request = request
        self.client_address = client_address

    # 没有实现，留给具体业务逻辑实现
    def handle(self):
        pass


class StreamRequestHandler(BaseRequestHandler):
    def __init__(self, server, request, client_address):
        BaseRequestHandler.__init__(self, server, request, client_address)
        self.wbuf = []      # 定义缓存区
        self.rfile = self.request.makefile('rb')        # unix 一切皆文件
        self.wfile = self.request.makefile('wb')

    # 编码。字符串->字节码
    def encode(self, msg):
        # 判断msg是否为字节码，不是则编码
        if not isinstance(msg, bytes):
            msg = bytes(msg, encoding='utf-8')
        return msg

    # 解码。字节码解码为字符串
    def decode(self, msg):
        if isinstance(msg, bytes):
            msg = msg.decode()
        return msg

    # 读
    def read(self, length):
        msg = self.rfile.read(length)
        return self.decode(msg)

    # 读行
    def readline(self, length=65536):   # http报文默认最大长度65536
        msg = self.rfile.readline(length).strip()
        return self.decode(msg)

    # 写内容到handler缓冲区
    def write_content(self, msg):
        msg = self.encode(msg)
        self.wbuf.append(msg)

    # 发送
    def send(self):
        for line in self.wbuf:
            self.wfile.write(line)
        self.wfile.flush()
        self.wbuf = []      # 清空缓冲

    # 关闭
    def close(self):
        self.wfile.close()
        self.rfile.close()
