#! /usr/bin/env python2

import multiprocessing as mp
import argparse
import subprocess

parser = argparse.ArgumentParser(description="Stress the VM network stack")

parser.add_argument('--host', dest="host")
parser.add_argument('--duration', type=int, dest="duration", default="20")
parser.add_argument('--ports', type=int, dest="ports", default="20")
parser.add_argument('--server', dest="server", action="store_true")

args = parser.parse_args()

def run_iperf_client(host, duration, port):
    print "Starting iperf pushing to host", host, "on port", port
    iperf_cmd = '/usr/bin/iperf -c {0} -t {1} -p {2} --reportstyle=c'.format(host, duration, port)
    subprocess.check_call(iperf_cmd.split())
   
def run_iperf_server(port):
    print "Starting iperf listening on port ", port
    iperf_cmd = '/usr/bin/iperf -s -p {0} --reportstyle=c'.format(port)
    subprocess.check_call(iperf_cmd.split())
    
def run_ping(host, count):
    print "Pinging host", host
    ping_cmd = '/bin/ping -c {0} {1}'.format(count, host)
    subprocess.check_call(ping_cmd.split())
    
def run_ping_server(host):
    print "Pinging host", host
    ping_cmd = '/bin/ping {0}'.format(host)
    subprocess.check_call(ping_cmd.split())

def main():
    processes = []
    print args.server
    if args.server is False:
        for i in range(args.ports):
            p = mp.Process(target=run_iperf_client, args=(args.host, args.duration, 5001 + i))
            p.start()
            processes.append(p)
        p = mp.Process(target=run_ping, args=(args.host, args.duration))
        p.start()
        processes.append(p)
    else:
        for i in range(args.ports):
            p = mp.Process(target=run_iperf_server, args=(5001 + i,))
            p.start()
            processes.append(p)
        p = mp.Process(target=run_ping_server, args=(args.host,))
        p.start()
        processes.append(p)
    
if __name__ == '__main__':
    main()