import time
import dpkt
import socket
import argparse

def make_icmp_socket(ttl, timeout):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
    sock.settimeout(timeout)
    return sock
    
def send_icmp_echo(socket, payload, id, seq, destination):
    echo = dpkt.icmp.ICMP.Echo() 
    echo.id = id
    echo.seq = seq
    echo.payload = payload

    icmp = dpkt.icmp.ICMP()
    icmp.type = dpkt.icmp.ICMP_ECHO
    icmp.data = echo
    socket.sendto(bytes(icmp),(destination,0))

def recv_icmp_response(ttl):
    newsocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    newsocket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
    (bytes, address) = newsocket.recvfrom(1000)
    return (bytes, address)

def ping(destination, ttl, timeout, n):
    totalRTT = 0
    successfulPing = 0
    for seq in range(n):
        sock = make_icmp_socket(ttl, timeout)
        # Make payload 
        payload = bytearray()
        # load payload with A,B,C... (soemthing random becuase it was not specified)
        for i in range(26):
            payload.append(0x41 + 1)
        id = seq

        send_icmp_echo(sock, payload, id, seq, destination)
        # start time when echo is called
        startTime = time.time()
    
        # using try so that we can throw exception if there is a timeout (idk if necessary)
        try:
            response = recv_icmp_response(ttl)
          # end time when a response is recieved
            endTime = time.time()
            rtt = (endTime-startTime) * 1000
            
            totalRTT = totalRTT + rtt
            successfulPing = successfulPing + 1

            print(f"destination = {destination}; icmp_seq = {seq}; icmp_id = {id}; ttl = {ttl}; rtt={rtt:.2f}ms")
    
        except socket.timeout:
    
            print(f"icmp_seq={seq} Request Timed out")
    
    average_rtt = round(totalRTT/n, 1)
    print(f"Average rtt: {average_rtt} ms; {successfulPing}/{n} succesful pings.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="ping")
    parser.add_argument("-destination", type=str)
    parser.add_argument('-n', type=int)
    parser.add_argument("-ttl",type=int)
    args = parser.parse_args()

    ttl = args.ttl
    id = 0
    timeout = 5 #if no response in 5 seconds then timeout 
    ping(args.destination, args.ttl, timeout, args.n)
