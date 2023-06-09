import xiaomiandns
import yaml


if __name__ == '__main__':
    with open('server/serverconf.yaml', 'r') as f:
        config = yaml.safe_load(f)
    db_file = config['database']['db_file']
    DNS_port = config['DNS']['port']
    DNS_listen_host = config['DNS']['listen_host']
    API_port = config['API']['port']
    API_listen_host = config['API']['listen_host']

    # start dns server
    server = xiaomiandns.DNSServer(DNS_listen_host, DNS_port, db_file)
    server.run()

    # start dns api server
    APIserver = xiaomiandns.DNSAPI(API_listen_host, API_port, db_file)
    APIserver.run()
