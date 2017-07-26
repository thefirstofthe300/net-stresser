#! /usr/bin/env python2

import multiprocessing as mp
import argparse
import subprocess
import time
from random import randint

parser = argparse.ArgumentParser(description="Stress the VM network stack")

parser.add_argument('--host', dest="host")
parser.add_argument('--duration', type=int, dest="duration", default="20")
parser.add_argument('--ports', type=int, dest="ports", default="20")
parser.add_argument('--server', dest="server", action="store_true")

args = parser.parse_args()

def run_iperf_client(host, duration, port):
    iperf_cmd = '/usr/bin/trickle -u 62500 -d 62500 iperf -c {0} -t {1} -p {2} --reportstyle=c'.format(host, duration, port)
    subprocess.check_call(iperf_cmd.split())
    
def run_iperf_server(port):
    iperf_cmd = '/usr/bin/iperf -s -p {0} --reportstyle=c'.format(port)
    subprocess.check_call(iperf_cmd.split())
    
def run_ping(host, count):
    ping_cmd = '/bin/ping -c {0} {1}'.format(count, host)
    subprocess.check_call(ping_cmd.split())
    
def run_ping_server(host):
    ping_cmd = '/bin/ping {0}'.format(host)
    subprocess.check_call(ping_cmd.split())

def main():
    processes = []
    if args.server is False:
        for i in range(args.ports):
            p = mp.Process(target=run_iperf_client, args=(args.host, randint(1, 9), 5001 + i))
            p.start()
            processes.append(p)
            
        timer=0
        p = mp.Process(target=run_ping, args=(args.host, args.duration))
        p.start()
        
        while(timer < args.duration):
            alive_processes = 0
            started_processes = 0
            for i in range(len(processes)):
                if not processes[i].is_alive():
                    alive_processes += 1
                elif timer % 5 == 0:
                    del processes[i]
                    length = randint(1, 9)
                    p = mp.Process(target=run_iperf_client, args=(args.host, length, 5001 + i))
                    p.start()
                    processes.insert(i, p)
                    started_processes += 1
            print "Alive processes:", alive_processes
            print "Started", started_processes, "processes."
        
            timer += 1
            time.sleep(1)
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
