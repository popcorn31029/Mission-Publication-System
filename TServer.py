#%%
import threading
from MsgHandle import handle
from AccountManage import AccountManage
from MissionManage import MissionManage

#%%
class MyServer(threading.Thread):
    
    def __init__(self, c_socket, c_adr):
        
        threading.Thread.__init__(self)
        self.socket = c_socket
        self.address= c_adr
        
    def run(self):
        
        print(threading.currentThread().name, 'start working')
        
        try:
            #%% if signin success, break
            while True:
                    
                account_msg = str(self.socket.recv(1024), encoding='Big5')
                account_msg = handle(account_msg)
                
                if account_msg['type'] == 'account':
                    
                    user = AccountManage(account_msg['account'], account_msg['password'])
                    if account_msg['mov'] == 'regist':          #if sign up
                        
                        signup_msg = user.signup(account_msg['username'])
                        self.socket.sendall(signup_msg.encode('Big5'))
                        continue
                    
                    elif account_msg['mov'] == 'signin':
                        
                        signin_msg = user.signin()
                        if 'success' in signin_msg:
                            self.socket.sendall(signin_msg.encode('Big5'))
                            break
                        
                        else:
                            self.socket.sendall(signin_msg.encode('Big5'))
                            continue
                        
            print('client can start to use mission system')
            
            #%% Mission System
            while True:
                    
                    mission_msg = str(self.socket.recv(1024), encoding='Big5')
                    mission_msg = handle(mission_msg)

                    if mission_msg['type'] == 'mission':
                        
                        mission = MissionManage()
                        #mission create 
                        if mission_msg['mov'] == 'create':          
                            create_msg = mission.create(mission_msg, user.account)
                            self.socket.sendall(create_msg.encode('Big5'))
                            continue
                        
                        #%% mission search
                        elif mission_msg['mov'] == 'search':
                            
                            if mission_msg['agpk'] != 'keyword':
                                search_msg = mission.search(user.account, mission_msg['agpk'])
                            elif mission_msg['agpk'] == 'keyword':
                                search_msg = mission.search_keyword(mission_msg['mdc'], mission_msg['tar'])
                            self.socket.sendall(search_msg.encode('Big5'))
                            continue
    
                        #%% mission detail
                        elif mission_msg['mov'] == 'detail':
                            
                            detail_msg = mission.detail(user.account, mission_msg['missionname'])
                            self.socket.sendall(detail_msg.encode('Big5'))
                            continue
    
                        #%% mission get
                        elif mission_msg['mov'] == 'get':
                            
                            score = user.good + user.bad
                            get_msg = mission.get(user.account, score, mission_msg['missionname'])
                            self.socket.sendall(get_msg.encode('Big5'))
                            continue
    
                        #%% mission complete
                        elif mission_msg['mov'] == 'complete':
                            
                            complete_msg = mission.complete(user.account, mission_msg['missionname'])
                            self.socket.sendall(complete_msg.encode('Big5'))
                            continue
                        
                        #%% mission score
                        elif mission_msg['mov'] == 'score':

                            score_msg = mission.score(mission_msg['missionname'], mission_msg['score'])
                            self.socket.sendall(score_msg.encode('Big5'))
                            continue
                            
        #%% disconnect
        except Exception:
            self.socket.close()
            print(threading.currentThread().name, 'disconnect')
            return  
