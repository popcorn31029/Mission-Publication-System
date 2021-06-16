#%%
import json
import threading

#%%
lock = threading.Lock()

#%%
class MissionManage:
    
    def __init__(self):  
        1 == 1
    
    #%% mission create
    def create(self, mission_data, account):

        mission_data['postaccount'] = account
        mission_data['getaccount'] = 'none'
        mission_data['complete'] = False        
        mission_data['score'] = False

        lock.acquire()
        try:
            with open ('./json/mission_info.json', 'r') as json_file:
                data = json.load(json_file)
        except Exception:
            data = list()

        with open ('./json/mission_info.json', 'w') as json_file:
            data.append(mission_data)
            json.dump(data, json_file)
            
        lock.release()
        
        print('Mission Create Success')
        create_msg = 'mission create success ' + mission_data['missionname']
        
        return create_msg       # mission create Success

    #%% mission search
    def search(self, account, agp):
        
        #self.missionsearch = ''
        search_msg = 'mission search'
        try:
            with open ('./json/mission_info.json', 'r') as json_file:
                mission_data = json.load(json_file)

            for mission in mission_data:
                if not mission['score']:
                    if agp == 'all':
                        if mission['getaccount'] == 'none':
                            search_msg += ' ' + mission['missionname']
                    
                    elif agp == 'get':
                        if account == mission['getaccount']:
                            search_msg += ' ' + mission['missionname']
                    
                    elif agp == 'post':
                        if account == mission['postaccount']:
                            search_msg += ' ' + mission['missionname']

        except Exception:    
            pass
        
        return search_msg
    
    #%% mission search keyword
    def search_keyword(self, mdc, tar):
        
        #self.missionsearch = ''
        search_msg = 'mission search'
        try:
            with open('./json/mission_info.json', 'r') as json_file:
                mission_data = json.load(json_file)

            for mission in mission_data:
                if not mission['score']:
                    if tar in mission[mdc]:
                        search_msg += ' ' + mission['missionname']
                                             
        except Exception:    
            pass

        return search_msg

    #%% mission detail
    def detail(self, account, missionname):
        
        #self.missiondetail = ''
        detail_msg = 'mission detail'
        try:
            with open ('./json/mission_info.json', 'r') as json_file:
                mission_data = json.load(json_file)
                
            for mission in mission_data:
                if missionname == mission['missionname']:
                    
                    if account == mission['postaccount'] and mission['complete'] and not mission['score']:
                        detail_msg += ' scorable'
                    
                    else:
                        detail_msg += ' nonscorable'
                    
                    with open('./json/user_info.json', 'r') as json_file:
                        user_data = json.load(json_file)
                    
                    for user in user_data:
                        if user['account'] == mission['postaccount']:
                            post_username = user['username']
                            
                    detail_msg += ' ' + post_username \
                                 + ' ' + mission['missionname'] \
                                 + ' ' + mission['destination'] \
                                 + ' ' + mission['deadline'] \
                                 + ' ' + mission['salary'] \
                                 + ' ' + mission['content']
                    print('Mission Detail Success')
                    return detail_msg

        except Exception:    
            pass
        
        print('Mission Detail Fail')
        return detail_msg + ' fail'

    #%% mission get
    def get(self, account, userscore, missionname):
        
        #if_sus_get = False
        get_msg = 'mission get'
        
        lock.acquire()
        try:
            with open ('./json/mission_info.json', 'r') as json_file:
                mission_data = json.load(json_file)
                
            for mission in mission_data:
                if mission['missionname'] == missionname and mission['getaccount'] == 'none':
                    if account != mission['postaccount'] and userscore >= -3:
                        
                        mission['getaccount'] = account
                        #if_sus_get = True
                        get_msg += ' success ' + missionname
                        
                        with open('./json/mission_info.json', 'w') as json_file:
                            json.dump(mission_data, json_file)
                        
                        lock.release()
                        print('Mission Get Success')
                        return get_msg

        except Exception:    
            pass
        
        lock.release()
        
        if userscore < -3:
            print('Mission score fail')
        else:
            print('Mission Get Fail')
        
        return get_msg + ' fail'

    #%% mission complete
    def complete(self, account, missionname):
        
        complete_msg = 'mission complete'
        
        lock.acquire()
        try:
            with open ('./json/mission_info.json', 'r') as json_file:
                mission_data = json.load(json_file)
                
            for mission in mission_data:
                if account == mission['getaccount'] and missionname == mission['missionname']:
                    mission['complete'] = True
                    complete_msg += ' ' + missionname
                    
                    with open('./json/mission_info.json', 'w') as json_file:
                        json.dump(mission_data, json_file)
                    
                    lock.release()
                    print('Mission Complete Success')
                    return complete_msg

        except Exception:    
            pass
        
        lock.release()
        print('Mission Complete Fail')
        return complete_msg +' fail'
    
    #%% mission score
    def score(self, missionname, score):
        
        score_msg = 'mission score'
        
        with open ('./json/mission_info.json', 'r') as json_file:
            mission_data = json.load(json_file)
        
        for mission in mission_data:
            if mission['missionname'] == missionname:
                if not mission['score']:
                    score_dest = mission['getaccount']
                    mission['score'] = True

                else:
                    return score_msg + ' fail'
            
        lock.acquire()
        
        with open ('./json/user_info.json', 'r') as json_file:
            user_data = json.load(json_file)
            
        for user in user_data:
            if user['account'] == score_dest:
                if score == 1:
                    user['good'] += 1
                
                elif score == -1:
                    user['bad'] += -1
                    
                break
        
        with open('./json/user_info.json', 'w') as json_file:
            json.dump(user_data, json_file)
        
        with open('./json/mission_info.json', 'w') as json_file:
            json.dump(mission_data, json_file)
        
        lock.release()
        
        return score_msg + ' success'
