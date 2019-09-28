# -*- encoding=utf-8 -*-


import socket
import threading


class TCPServer:

    def __init__(self, server_address, handler_class):
        self.server_address = server_address
        self.HandlerClass = handler_class
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # 参数1协议，参数2指定字节流
        self.is_shutdown = False

    # 服务器启动函数
    def serve_forever(self):
        self.socket.bind(self.server_address)
        self.socket.listen(10)
        while not self.is_shutdown:
            # 1.接收请求
            request, client_address = self.get_request()
            # 2.处理请求，需要捕获异常。这里是阻塞式的处理请求
            try:
                # self.process_request(request, client_address)
                self.process_request_multithread(request, client_address)
            except Exception as e:
                print(e)
            #finally:
                # 3.关闭请求
                # self.close_request(request)  使用多线程不能在主循环里关闭request，有可能主循环将其关闭了而处理线程中却没处理完，应搬移至处理函数
        pass

    # 接收请求
    def get_request(self):
        return self.socket.accept()

    # 处理请求
    def process_request(self, request, client_address):
        handler = self.HandlerClass(self, request, client_address)
        handler.handle()
        # 3.关闭请求
        self.close_request(request)

    # 多线程处理请求
    def process_request_multithread(self, request, client_address):
        t = threading.Thread(target=self.process_request, args=(request, client_address))
        t.start()

    # 关闭请求
    def close_request(self, request):
        request.shutdown(socket.SHUT_WR)
        request.close()

    # 关闭服务器
    def shutdown(self):
        self.is_shutdown = True     # 跳出循环标志
        pass
