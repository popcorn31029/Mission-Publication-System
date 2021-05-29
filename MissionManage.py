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
    def create(self, missionname, destination, deadline, salary, content, postname):

        self.missionname = missionname
        self.destination = destination
        self.deadline = deadline
        self.salary = salary
        self.content = content
        self.postname = postname
        self.getname = 'none'

        mission_dict = {'missionname' : self.missionname,
                        'destination' : self.destination,
                        'deadline' : self.deadline,
                        'salary' : self.salary,
                        'content' : self.content,
                        'postname' : self.postname,
                        'getname' : self.getname}
        
        lock.acquire()
        try:
            with open ('mission_info.json', 'r') as json_file:
                data = json.load(json_file)
        except Exception:
            data = list()

        with open('mission_info.json', 'w', ) as json_file:
            data.append(mission_dict)
            json.dump(data, json_file)
            
        lock.release()

        return True     #mission create Success


    #%% mission search
    def search(self, username, agp):
        
        mission_list = ''
        try:
            with open('mission_info.json', 'r') as json_file:
                mission_data = json.load(json_file)
                
            if agp == 'all':
                for mission in mission_data:
                    mission_list += (' ' + mission['missionname'])
            elif agp == 'get':
                for mission in mission_data:
                    if username == mission['getname']:
                        mission_list += (' ' + mission['missionname'])
            elif agp == 'post':
                for mission in mission_data:
                    if username == mission['postname']:
                        mission_list += (' ' + mission['missionname'])
            self.missionlist = mission_list

        except Exception:    
            pass
        
        return True

    #%% mission detail
    def detail(self, missionname):
        
        mission_detail = ''
        try:
            with open('mission_info.json', 'r') as json_file:
                mission_data = json.load(json_file)
            for mission in mission_data:
                if missionname == mission['missionname']:
                    mission_detail = ' ' + mission['missionname'] + ' ' + mission['destination'] + ' ' + mission['deadline'] + ' ' + mission['salary'] + ' ' + mission['content']
                    break
            self.missiondetail = mission_detail

        except Exception:    
            pass
        
        return True

    #%% mission get
    def get(self, username, missionname):
        
        lock.acquire()
 
        try:
            with open('mission_info.json', 'r') as json_file:
                mission_data = json.load(json_file)
            for mission in mission_data:
                if username != mission['postname'] and missionname == mission['missionname']:
                    mission['getname'] = username
                    break

        except Exception:    
            pass
        
        with open('mission_info.json', 'w', ) as json_file:
            json.dump(mission_data, json_file)

        lock.release()

        return True

    #%% mission complete
    def cmoplete(self, username, missionname):
        
        lock.acquire()
 
        try:
            with open('mission_info.json', 'r') as json_file:
                mission_data = json.load(json_file)
            for mission in mission_data:
                if username == mission['getname'] and missionname == mission['missionname']:
                    mission_data.remove(mission)
                    break

        except Exception:    
            pass
        
        with open('mission_info.json', 'w', ) as json_file:
            json.dump(mission_data, json_file)

        lock.release()
        
        return True