import socket
import ssl
from cymruwhois import Client

HOST = "127.0.0.1"
PORT = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))

#Returns the IPv4 address of domain specified in the command.
def IPV4_ADDR(domain):
    try:
      IPv4 = socket.gethostbyname(domain)
      return IPv4
    except:
        return ("Error: No IPv4 Address Associated with Domain")
    
#Returns the IPv6 address of domain specified in the command.
def IPV6_ADDR(domain):
    try:
        IPv6 = (socket.getaddrinfo(domain, None, socket.AF_INET6)[0][4][0])
        return IPv6
    except:
        return ("Error: No IPv6 Address Associated with Domain")

#Returns the TLS/SSL certificate associated with the domain specified in the command.
def TLS_CERT(domain):
    context = ssl.create_default_context()
    try:
        wrappedSocket = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname = domain)
        wrappedSocket.connect((domain, 443))
        cert = wrappedSocket.getpeercert(False)
    except:
        return ("Error: Invalid Domain Entered")
    if len(cert) == 0:
        return "Certificate Not Validated"
    else:
        return cert

#Returns the name of the Autonomous System that hosts the IP address associated with the domain 
#specified in the command.
def HOSTING_AS(domain):
    try:
        IP = socket.gethostbyname(domain)
    except:
        return ("Error: Invalid Domain Entered")
    client = Client()
    AS = client.lookup(IP)
    return AS.owner

#Returns the name of the organization associated with the domain specified in the command.
def ORGANIZATION(domain):
    cert = TLS_CERT(domain)
    if cert=="Certificate Not Validated" or cert=="Error: Invalid Domain Entered":
        return(cert)
    else:
        subValues = cert['subject']
        newDict = dict(kValues[0] for kValues in subValues)
        try:
            orgName = newDict['organizationName']
        except:
            orgName = "Organization Not Available"
        return orgName