import socket
import socketserver
import struct
import select

class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class Socks5Handler(socketserver.BaseRequestHandler):
    VERSION = 5

    def handle(self):
        # 客户端发送版本和方法
        version, nmethods = struct.unpack('!BB', self.request.recv(2))
        self.request.recv(nmethods)

        # 发送版本和方法响应
        self.request.sendall(struct.pack('!BB', self.VERSION, 0))

        # 获取请求详情
        version, cmd, _, address_type = struct.unpack('!BBBB', self.request.recv(4))
        if address_type == 1:  # IPv4
            address = socket.inet_ntoa(self.request.recv(4))
        else:
            raise NotImplementedError('Only IPv4 is supported.')
        port = struct.unpack('!H', self.request.recv(2))[0]

        # 发送响应
        self.request.sendall(struct.pack('!BBBBIH', self.VERSION, 0, 0, 1,
                                         int(socket.inet_aton('0.0.0.0').hex(), 16), 0))

        # 建立连接
        if cmd == 1:  # CONNECT
            remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote.connect((address, port))
            self.exchange_loop(self.request, remote)
        else:
            raise NotImplementedError('Only CONNECT is supported.')

    def exchange_loop(self, client, remote):
        while True:
            # Simple data exchange between client and remote
            rlist, _, _ = select.select([client, remote], [], [])
            if client in rlist:
                data = client.recv(4096)
                if remote.send(data) <= 0:
                    break
            if remote in rlist:
                data = remote.recv(4096)
                if client.send(data) <= 0:
                    break

if __name__ == '__main__':
    with ThreadingTCPServer(('0.0.0.0', 1080), Socks5Handler) as server:
        server.serve_forever()
