import xiaomiandns
import yaml


if __name__ == '__main__':
    with open('serverconf.yaml', 'r') as f:
        config = yaml.safe_load(f)
    db_file = config['database']['db_file']
    DNS_port = config['DNS']['port']
    DNS_listen_host = config['DNS']['listen_host']
    API_port = config['API']['port']
    API_listen_host = config['API']['listen_host']

    DNSServer = xiaomiandns.DNSServer(listen_host, DNS_port, db_file)
    DNSServer.run()
