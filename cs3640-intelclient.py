import argparse
import pprint
server = __import__("cs3640-intelserver")

parser = argparse.ArgumentParser(description = "client")
parser.add_argument("-intel_server_addr", type = str, required = True, default = "127.0.0.1")
parser.add_argument("-intel_server_port", type = int, required = True, default = 5555)
parser.add_argument("-domain", type = str, required = True)
parser.add_argument("-service", type = str, required = True)
args = parser.parse_args()

intel_server_addr = args.intel_server_addr
intel_server_port = args.intel_server_port
domain = args.domain
service = args.service

if intel_server_addr == "127.0.0.1" and intel_server_port == 5555:
    try:
        if service == "IPV4_ADDR":
            x = server.IPV4_ADDR(domain)
        elif service == "IPV6_ADDR":
            x = server.IPV6_ADDR(domain)
        elif service == "TLS_CERT":
            x = server.TLS_CERT(domain)
        elif service == "HOSTING_AS":
            x = server.HOSTING_AS(domain)
        elif service == "ORGANIZATION":
            x = server.ORGANIZATION(domain)
        else:
            x = "Error: Invalid Service"
    except:
        x = "Error: Invalid Domain"
else:
    x = "IP and or Port do not match the intel server"
pprint.pprint(x)
