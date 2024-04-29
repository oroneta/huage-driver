#!/bin/python3
import os,sys,time,socket
import numpy as np
 
UDP_PKT_SIZE= 2000

receive = False
 
out_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
out_sock.bind(('0.0.0.0', 6666))
out_sock.setblocking(0)
out_sock.settimeout(8)

'''
66 80 80 80 80 00 00 99 = Normal Mode
66 80 80 00 94 00 94 99 = Z-Mode
66 80 80 80 80 10 10 99 = Forward back left right Mode
66 80 80 80 80 01 01 99 = Up
66 80 80 80 80 02 02 99 = Down

66 80 80 80 80 04 04 99 = Stop
'''
 

# Fork
pid = os.fork()

# if (pid == 0):
#     # Child
#     while 1:
#         out_sock.sendto(b'\x66\x80\x80\x80\x80\x00\x00\x99',("192.168.4.153", 8090))
#         time.sleep(0.5)

#     exit(0)

# else:
#     for i in range(10):
#         out_sock.sendto(b'\x66\x80\x80\x80\x80\x00\x00\x99',("192.168.4.153", 8090))

#     # if abort ctrl+c, kill child
#     try:
#         os.waitpid(pid, 0)
#     except KeyboardInterrupt:
#         os.kill(pid, 9)

for i in range(10):
    out_sock.sendto(b'\x66\x80\x80\x80\x80\x00\x00\x99',("192.168.4.153", 8090))
    time.sleep(0.1)

for i in range(20):
    out_sock.sendto(b'\x66\x80\x80\x80\x80\x04\x04\x99',("192.168.4.153", 8090))
    time.sleep(0.1)

for i in range(10):
    out_sock.sendto(b'\x66\x80\x80\x80\x80\x00\x00\x99',("192.168.4.153", 8090))
    time.sleep(0.1)

 
 