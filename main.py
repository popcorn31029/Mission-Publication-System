#%%
import socket
from TServer import MyServer

#%%
if __name__ == '__main__':
    
    HOST = '127.0.0.1'
    PORT = 8000
    
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_socket.bind((HOST, PORT))
    s_socket.listen(5)
    print('Sever ir ready')
    
    while True:
        
        c_socket, c_adr = s_socket.accept()
        MyServer(c_socket, c_adr).start()