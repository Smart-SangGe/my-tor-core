import socket
import threading
import dns.resolver
import dns.message
import dns.rdataclass
import dns.rdatatype
import dns.flags
import dns.rcode
import dns.rrset
import time
import sqlite3
import re


class DNSServer:
    def __init__(self, hostname, port, db_file):
        self.hostname = hostname
        self.port = port
        self.db_file = db_file

    def run(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind((self.hostname, self.port))
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.bind((self.hostname, self.port))
        self.tcp_socket.listen(1)
        print(f"DNS server running on {self.hostname}:{self.port}")
        for i in range(3):
            udp_thread = threading.Thread(target=self.handle_udp_request)
            udp_thread.start()
            tcp_thread = threading.Thread(target=self.handle_tcp_request)
            tcp_thread.start()

    def handle_udp_request(self):
        data, address = self.udp_socket.recvfrom(1024)
        response = self.handle_request(data)
        self.udp_socket.sendto(response, address)
        udp_thread = threading.Thread(target=self.handle_udp_request)
        udp_thread.start()

    def handle_tcp_request(self):
        connection, address = self.tcp_socket.accept()
        data = connection.recv(1024)
        response = self.handle_request(data)
        connection.send(response)
        connection.close()
        tcp_thread = threading.Thread(target=self.handle_tcp_request)
        tcp_thread.start()

    def handle_request(self, data):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        question = dns.message.from_wire(data)
        response = self.build_response(question, cur)
        return response

    def build_response(self, question, dbcursor, rcode=dns.rcode.NOERROR, answer=None):
        # Create a new DNS message object
        response = dns.message.Message()

        # Set the message header fields
        response.id = question.id
        response.flags = dns.flags.QR | dns.flags.RA

        # Add the question to the message
        response.question = question.question

        name = question.question[0].name
        # search domain in database
        dbcursor.execute(
            "SELECT ip FROM xiaomiandns WHERE domain = ?", (str(name)[:-1],))
        result = dbcursor.fetchone()

        # Create a new RRset for the answer
        if result is not None:
            answer = dns.rrset.RRset(name, dns.rdataclass.IN, dns.rdatatype.A)
            rdata = dns.rdata.from_text(
                dns.rdataclass.IN, dns.rdatatype.A, result[0])
            answer.add(rdata)
            response.answer.append(answer)
            # Set the response code
            response.set_rcode(rcode)
        else:
            response.set_rcode(dns.rcode.NXDOMAIN)
        return response.to_wire()


class DNSAPI:
    # usage: /add?domian=xxxx&ip=xx.xx.xx.xx&key=xxxxx
    #        /delete?domian=xxxx&ip=xx.xx.xx.xx&key=xxxxx
    
    def __init__(self, hostname, port, db_file):
        self.hostname = hostname
        self.port = port
        self.db_file = db_file


    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定 IP 地址和端口号
        server_socket.bind((self.hostname, self.port))
        # 监听连接
        server_socket.listen(5)
        print(f"API server running on {self.hostname}:{self.port}")
        while True:
            # 接受连接
            conn, addr = server_socket.accept()
            # 处理请求
            t = threading.Thread(target=self.handle_tcp_request, args=(conn,))
            t.start()
            
    def handle_tcp_request(self,conn):
        request = conn.recv(1024).decode('utf-8')
        response = self.handle_http_request(request)
        conn.send(response)
        conn.close()

    def handle_http_request(self, request):
        request_line, headers= request.split('\r\n\r\n', 2)
        method, url, version = request_line.split(' ', 2)
        print(method,url)
        if method == 'GET':
            response = self.handle_get_request(url)
        else:
            response = self.handle_error_request()
        return response

    def handle_get_request(self, url):
        # check url start with /add
        if re.match(r'^/add\?',url):
            status_code = self.add_data(url[5:])
            if status_code = 200:
                reason_phrase = 'Add data successful'
            else:
                reason_phrase = 'Add data unsuccessful'
        # check url start with /delete        
        elif re.match(r'^/delete\?',url):
            status_code = self.delete_data(url[9:])
            if status_code = 200:
                reason_phrase = 'Delete data successful'
            else:
                reason_phrase = 'Delete data unsuccessful'
        else:
            status_code = 400
            reason_phrase = 'unsupport api'
            
        headers = {
        'Content-Type': 'text/html',
        'Connection': 'close',
        }
        response = 'HTTP/1.1 {} {}\r\n'.format(status_code, reason_phrase)
        return response.encode("utf-8")

    def handle_error_request(self, request):
        status_code = 400
        reason_phrase = "unsupport method"
        headers = {
        'Content-Type': 'text/html',
        'Connection': 'close',
        }
        response = 'HTTP/1.1 {} {}\r\n'.format(status_code, reason_phrase)
        return response.encode("utf-8")
    
    def add_data(self, url):
        domain = re.search(r'domain=([^&]+)', url)
        ip = re.search(r'ip=([^&]+)', url)
        key = re.search(r'ip=([^&]+)', url)
        if domain and ip and key:
            domain = domain.group(1)
            ip = ip.group(1)
            key = key.group(1)
        else:
            return 400
        return 200
    
    def delete_data(self,url):
        m = re.search(r'domain=([^&]+)', url)
        if m:
            domain = m.group(1)
            print(domain)
        else:
            print('not matched')
        return 200
        


if __name__ == '__main__':
    # some config
    db_file = '../database/dns.db'
    DNS_port = 53
    listen_host = "0.0.0.0"
    API_port = 81

    # start dns server
    server = DNSServer(listen_host, DNS_port, db_file)
    server.run()

    # start dns api server
    APIserver = DNSAPI(listen_host, API_port, db_file)
    APIserver.run()