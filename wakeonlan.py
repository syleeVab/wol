import struct
import socket

def wakeOnLan(mac) :
    addrs = mac.split('-')
    hw_addr = struct.pack("BBBBBB", int(addrs[0],16),
                          int(addrs[1],16),int(addrs[2],16),
                          int(addrs[3],16),int(addrs[4],16),
                          int(addrs[5],16)                          
                          )
    magic = b"\xFF" * 6 +hw_addr * 16
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
    s.sendto(magic, ('172.30.1.255',7))
    s.close()
    
wakeOnLan('B4-2E-99-4C-05-DF')

