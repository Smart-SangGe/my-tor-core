import xiaomiandns


if __name__ == '__main__':
    db_file = '../database/dns.db'
    DNS_port = 53
    listen_host= "0.0.0.0"
    
    DNSServer = xiaomiandns.DNSServer(listen_host, DNS_port, db_file)
    DNSServer.run()
