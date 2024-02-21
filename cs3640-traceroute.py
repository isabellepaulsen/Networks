import time
import dpkt
import socket
import importlib
moduleping = importlib.import_module("cs3640-ping")
import argparse

def traceroute(destination, n_hops):
    for seq in range (1, n_hops + 1):
        #set ttl to increment every time
        ttl = seq
        timeout = 5

        #make socket
        sock = moduleping.make_icmp_socket(ttl, timeout)

        # Make payload 
        payload = bytearray()
        # load payload with A,B,C... (soemthing random becuase it was not specified)
        for i in range(26):
            payload.append(0x41 + 1)
        
        #send packet    
        moduleping.send_icmp_echo(sock, payload, seq, seq, destination)
        # start time when echo is called
        startTime = time.time()
        
        response = moduleping.recv_icmp_response(ttl)
        # end time when a response is recieved
        endTime = time.time()
        rtt = (endTime-startTime) * 1000

        #set IP address to the hop that sends back timeout
        ip = response[1][0]

        print(f"destination = {destination}; hop {seq} = {ip}; rtt = {rtt:.2f}ms")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-destination", type = str)
    parser.add_argument("-n_hops", type = int)
    args = parser.parse_args()
    traceroute(args.destination, args.n_hops)
