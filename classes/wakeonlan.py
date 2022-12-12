import struct
import socket

# 서버코드? 클라이언트 코드?
# 참고 : https://gist.github.com/ninedraft/7c47282f8b53ac015c1e326fffb664b5 
# https://www.daniweb.com/programming/software-development/threads/132968/how-to-send-broadcast-message-over-network-and-collect-all-the-ipaddress,
#  https://itsaessak.tistory.com/125 , https://www.it-note.kr/122 
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
    
    