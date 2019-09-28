# python-simpleHttpServer
a simple http server implemented by python

参考教程：<https://imooc.com/learn/1172>

## 类继承关系（自上而下）：

`                                    **BaseRequestHandler**
                                                      
**TCPServer** --------------------- **StreamRequestHandler**

**BaseHTTPServer** --------------- **BaseHTTPRequestHandler**

**SimpleHTTPServer** ------------ **SimpleHTTPRequestHandler**

## TCP协议

TCP/IP四层模型：网络接口层、网络层(IP协议)、传输层(TCP协议)、应用层(HTTP协议)

ps: 括号内只是代表，不是全部。

TCP(传输控制协议)：可靠传输、流量控制、拥塞控制

**TCP报文：**

【TCP首部】【TCP数据报的数据】

数据报数据就是应用层的报文。

TCP是**面向字节流的协议**，也就是说无论传输的是图片还是文字还是别的什么，都需要转为字节数组也就是字节流来传输。

**网络套接字与通信过程:**

客户端与服务端之间的通信、节点间的通信最终都是进程间的通信，而进程间网络通信时使用端口(0~65535)作标志，
而IP标记一台计算机，所以`{IP:Port}`可以用来标记网络通信一端的进程，也被称为套接字(Socket)
通过套接字可以进行数据通信。

服务端套接字编程：
创建套接字 ——> 绑定套接字 ——> 监听套接字 ——> 处理信息
客户端编程：
创建套接字 ——> 连接套接字 ——> 处理信息



## HTTP协议

HTTP：超文本传输协议

WEB 1.0 访问资源； WEB2.0 操作资源

常用操作：GET POST PUT UPDATE DELETE

**浏览器访问服务器流程：**

    浏览器发起HTTP请求 ——> 服务器接收客户端连接 ——> 接收请求报文 ——> 处理请求
    ——> 访问Web资源 ——> 构造应答 ——> 发送应答 ——> 浏览器收到HTTP应答

**HTTP请求报文：**

    【请求方法】【请求地址】【HTTP版本】
    
    【请求头】
    
    【请求内容】

请求行实例： GET /index.html HTTP/1.1

请求头为通道附加的信息，以k-v对形式存在，可以是多行，常见的请求头有'Content-Length'

**HTTP应答报文：**

    【HTTP版本】【状态码】【状态解释】
    
    【应答头】
    
    【应答内容】

