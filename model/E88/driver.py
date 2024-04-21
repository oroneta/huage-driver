#!/bin/python3
import os,sys,time,socket
import select
import cv2
import numpy as np
import struct, queue, _thread
 
UDP_PKT_SIZE= 2000

receive = False
 
out_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
out_sock.bind(('0.0.0.0', 6666))
out_sock.setblocking(0)
out_sock.settimeout(8)
 
def decode_jpeg(buf):
    try:
        img = cv2.imdecode(np.fromstring(buf, dtype=np.uint8) ,cv2.IMREAD_COLOR)
        cv2.imshow('IMG', img)
        if cv2.waitKey(1) == 27:
            exit(0)
        #img = Image.fromarray(np.fromstring(buf, dtype=np.uint8) )
        #cv2.imshow(img) 
    except Exception as e:
        print(">>>>>>>>>> imdecode error!", e)
        pass
      
def isValidJPEG():
    t_len = len(s_buf)
    if s_buf[0] == 0xff and s_buf[1] == 0xd8 and s_buf[t_len-1] == 0xd9 and s_buf[t_len-2] == 0xff:
        return True
    else:
        return False
  
def chk_tail(jpg_len, b_jpg_len):
    unpack_len = struct.unpack("<H", b_jpg_len)
    try:
        tail_jpeg_len = int(unpack_len[0])
        if tail_jpeg_len != jpg_len:
            print("Check tail failed.",tail_jpeg_len, jpg_len)
            return False
        else:
            return True
    except:
        return False
    pass
    
s_buf = b''
sn_old = 0
b_jpg_len=b''
 
udp_recv_buf_q  = queue.Queue()
 
 
def decode_jpeg_proc():
    global udp_recv_buf_q
    while 1:
        if not udp_recv_buf_q.empty():
            m_item = udp_recv_buf_q.get()
            rx_buf_len = len(m_item[0])
            
            if chk_tail(rx_buf_len, m_item[1]):
                decode_jpeg(m_item[0])
            else:
                print("#### CHECK FAILED ####")
                pass
        else:
            time.sleep(0.001)
        pass
        
_thread.start_new_thread(decode_jpeg_proc, (()))
 
while 1:
    if not receive:
        print("Comm try...")
        out_sock.sendto(b'\x42\x76',("192.168.4.153", 8080))
        out_sock.sendto(b'\xaa\x80\x80\x00\x80\x00\x80\x55',("192.168.4.153", 8090))

    try:
        rx_buf, addr = out_sock.recvfrom(UDP_PKT_SIZE)
        receive = True
    except socket.timeout:
        receive = False
        continue


    rv_len = len(rx_buf)
    print(rv_len)
    sn = rx_buf[0]
    isEof = rx_buf[1]
    if sn_old != sn:
        sn_old = sn
        if len(s_buf) == 0 :
            continue
        # #Finish a whole picture. Decode later.
        # print("Got a frame, try decode:",len(s_buf))
        # #Decode
        # decode_jpeg(s_buf)
        if not udp_recv_buf_q.full():
            if isValidJPEG():
                udp_recv_buf_q.put((s_buf, b_jpg_len))
            else:
                print("Not valid JPEG.")
                pass
        #Clear buffer
        s_buf = b''
     
    if isEof != 1:
        s_buf=s_buf+rx_buf[8:]
        pass
    else:
        s_buf=s_buf+rx_buf[8:rv_len-5]
        #Featch jpeg length, little endian ushort 
        b_jpg_len = rx_buf[rv_len-4:rv_len-2]
        time.sleep(0.001)
 
 