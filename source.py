#!/usr/bin/python3
import argparse
import logging,logging.handlers
import signal
import subprocess

import psutil
import time

import termcolor

logger = logging.getLogger(__name__)



def get_args(argv):

    def non_negative_int(x):
        i = int(x)
        if i < 0:
            raise ValueError('Negative values are not allowed')
        return i

    def percent_int(x):
        i = int(x)
        if i>0 and i<100:
            return i
        raise ValueError('Percent values allowed')


    parser = argparse.ArgumentParser(usage='...',
                                     description="System Sources Monitoring")

    parser.add_argument("-c","--cpu",
                        default=85, type=percent_int,
                        help="Shows cpu usage percentages (critical value default: 85)")

    parser.add_argument("-d","--disk",
                        default=85, type=percent_int,
                        help="Shows percent usage of '/' directory (critical value default: 85)")

    parser.add_argument("-n", "--network",
                        action="store_true",
                        help="Shows bandwidth usages as kB")

    parser.add_argument("-r", "--ram",
                        default=70, type=percent_int,
                        help="Shows ram usage percentage(critical value default: 70)")

    parser.add_argument("-s", "--syn",
                        default=100, type=non_negative_int,
                        help="Shows current SYN requests ")

    parser.add_argument("-p", "--ports",
                        default=100, type=non_negative_int,
                        help="Shows the number of IPs currently in communication on tcp/udp ports ")

    parser.add_argument("-t", "--time",
                        default=2, type=non_negative_int,
                        help="Settings up the resolution time")


    return parser.parse_args(argv)


def handle_logger():
    logger.setLevel(logging.WARNING)

    file_handler = logging.handlers.RotatingFileHandler(filename='/tmp/systemMonitor_logFile.log',
                                                       maxBytes=1024 * 1024, # 1MB
                                                       backupCount=3)

    formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s', datefmt='%d/%m/%Y -- %H:%M:%S')

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)



# cpu

def cpu_Usage():
    cpu = psutil.cpu_percent(interval=1, percpu=True)
    return cpu

# disk

def disk_Usage():
    disk = psutil.disk_usage('/').percent
    return disk

# network

def netload():
    netrcv = int((psutil.net_io_counters().bytes_recv)/1000000)
    netsent = int((psutil.net_io_counters().bytes_sent)/1000000)
    return (netrcv,netsent)

# ram

def ram_usage():
    ram = psutil.virtual_memory().percent
    return ram

#syn

def syn_Detecter():

    cmd_SYN = "netstat -ant | grep 'SYN' |  wc -l "

    syn_requests     =  subprocess.Popen(cmd_SYN,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output_SYN       =  syn_requests.communicate()[0]

    output_SYN = int(output_SYN)

    return (output_SYN)

#all ports

def allPortCommunication():

    cmd_all_ports = "netstat -ntu | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -n|wc -l"

    all_port_states  =  subprocess.Popen(cmd_all_ports,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output_aps       =  all_port_states.communicate()[0]

    output_aps = int(output_aps)

    return output_aps



def critical_evaluation(args):
    header_counter = 0
    while True:

        current_cpu = cpu_Usage()
        cpu_color = "blue"
        if max(current_cpu) > args.cpu:
            cpu_color="red"

        current_disk = disk_Usage()
        disk_color = "blue"
        if current_disk > args.disk:
            disk_color="red"

        current_net_rcv , current_net_sent = netload()


        current_ram = ram_usage()
        ram_color = "blue"
        if current_ram > args.ram:
            ram_color="red"

        current_syn = syn_Detecter()
        syn_color = "blue"
        if current_syn > args.syn:
            syn_color="red"

        current_communication = allPortCommunication()
        ports_color = "blue"
        if current_communication > args.ports:
            ports_color="red"

        if header_counter %10 == 0:
            print("|{:^47}|{:^11}|{:^12}|{:^21}|{:^9}|{:^11}|".format("CPU Usage",
                                                                       "RAM Usage",
                                                                       "DISK Usage",
                                                                       "Received / Sent KB",
                                                                       "SYN_RECV",
                                                                       "Contacted IPs"))

        for cpu in current_cpu:
            print(termcolor.colored("|  %{:^8}", cpu_color).format(cpu), sep="", end="")



        print(termcolor.colored("|  %{:^8}|", ram_color).format(current_ram),
              termcolor.colored("  %{:^8}|", disk_color).format(current_disk),
              termcolor.colored("{:^9}/", "blue").format(current_net_rcv),
              termcolor.colored("{:^8}", "blue").format(current_net_sent),
              termcolor.colored("|{:^9}|", syn_color).format(current_syn),
              termcolor.colored("{:^12}|", ports_color).format(current_communication-2))





        header_counter+= 1

        time.sleep(args.time)

_is_interrupted = False
def handle_sigint(sig, stack):
    """When user sends SIGINT (via Ctrl-C) we ask if it's sure or not"""
    global _is_interrupted  # If we're already interrupted, just exit and keep it in the global variables
    if _is_interrupted:
        exit(20)

    _is_interrupted = True

    choice = input("\rAre you sure you want to exit? (Y/n)").lower()

    if choice == "y" or choice == "":
        exit(0)


    _is_interrupted = False


def connect_signals():
    signal.signal(signal.SIGINT, handle_sigint)
    logger.info("Sigint connected")














