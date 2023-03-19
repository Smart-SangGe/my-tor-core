import dns.resolver


def resolver(domain):
    # 构造 DNS 查询请求
    qtype = 'A'

    # 发送 DNS 查询请求
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ["127.0.0.1"]

    try:
        ip = resolver.resolve(domain, qtype)[0]
        return ip
    except dns.resolver.NXDOMAIN:
        print("can't find IP")


if __name__ = "__main__":
    domain = 'mamahaha.work'
    ip = resolver(domain)
    print(ip)