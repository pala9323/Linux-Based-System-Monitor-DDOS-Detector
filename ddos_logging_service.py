#!/usr/bin/python3
import time,psutil
import source



source.handle_logger()


while True:
    syn  = source.syn_Detecter()
    port = source.allPortCommunication()

    if syn > 100:
        cpu = psutil.cpu_percent(interval=1, percpu=True)
        source.logger.warning("SYN_RECV: {} -- CPU(%): {}".format(syn,cpu))

    if port > 130:
        cpu = psutil.cpu_percent(interval=1, percpu=True)
        source.logger.warning("Connected IPs: {} -- CPU(%): {}".format(port,cpu))

    time.sleep(3)