#%%
def handle(msg_s):
    
    msg_l = msg_s.split()
    info = {'type' : msg_l[0],
            'mov' : msg_l[1]}
    
    if info['type'] == 'account':
        
        info['account'] = msg_l[2]
        info['password'] = msg_l[3]
        
        if info['mov'] == 'regist':    
            info['username'] = msg_l[4]
            
    elif info['type'] == 'mission':
        
        if info['mov'] == 'create':
            info['missionname'] = msg_l[2]
            info['destination'] = msg_l[3]
            info['deadline'] = msg_l[4]
            info['salary'] = msg_l[5]
            info['content'] = msg_l[6]
            
        elif info['mov'] == 'search':
            info['agpk'] = msg_l[2]
            if info['agpk'] == 'keyword':
                info['mdc'] = msg_l[3]
                info['tar'] = msg_l[4]
        
        elif info['mov'] == 'detail':
            info['missionname'] = msg_l[2]
            
        elif info['mov'] == 'get':
            info['missionname'] = msg_l[2]
            
        elif info['mov'] == 'complete':
            info['missionname'] = msg_l[2]
        
        elif info['mov'] == 'score':
            info['missionname'] = msg_l[2]
            info['score'] = int(msg_l[3])
            
    return info

#%% Only for test
if __name__ == '__main__':
    
    infos = list()
    
    msgs = list()
    msgs.append('account signin alan987 password')
    msgs.append('account regist jack1234 password jack')
    msgs.append('mission create write_python empty 6/16 100 finish_the_python_final_project')
    msgs.append('mission search all')
    msgs.append('mission search get')
    msgs.append('mission search post')
    msgs.append('mission detail write_python')
    msgs.append('mission get write_python')
    msgs.append('mission complete write_python')
    
    for msg in msgs:
        infos.append(handle(msg))