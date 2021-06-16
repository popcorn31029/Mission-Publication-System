#%%
import json
import threading

#%%
lock = threading.Lock()

#%%
class AccountManage:
    
    def __init__(self, account, password):  
        
        self.account = account
        self.password = password
        
    #%% Record the new user
    def signup(self, username):
        
        self.good = 0
        self.bad = 0
        signup_msg = 'account regist'
        self.username = username
        user_dict = {'username' : self.username,
                     'account' : self.account,
                     'password' : self.password,
                     'good' : self.good,
                     'bad' : self.bad
                     }
        
        lock.acquire()
        try:
            with open ('./json/user_info.json', 'r') as json_file:
                user_data = json.load(json_file)
        except Exception:
            user_data = list()
            
        if_same = self.check_if_same(user_data)
        if(if_same):
            lock.release()
            print('Signup Fail')
            return signup_msg + ' fail'    #There are the same account
        
        with open('./json/user_info.json', 'w') as json_file:
            user_data.append(user_dict)
            json.dump(user_data, json_file)
            
        lock.release()
        print('Signup Success')
        return signup_msg + ' success'     #Success signup
    
    #%%
    def signin(self):
        
        signin_msg = 'account signin'
        try:
            with open('./json/user_info.json', 'r') as json_file:
                user_data = json.load(json_file)
                
            for user in user_data:
                if(self.account == user['account'] and self.password == user['password']):
                    self.username = user['username']
                    self.good = user['good']
                    self.bad = user['bad']
                    
                    print('Signin Success')
                    return signin_msg + ' success ' + self.username + ' ' + str(self.good) + ' ' + str(self.bad)

        except Exception:    
            pass
        
        print('Signin Fail')
        return signin_msg + ' fail'

    #%%
    def check_if_same(self, data):
        
        for user in data:
            if(self.account == user['account']):
                return True
            
        return False
    
#%%
if __name__ == "__main__":
    
    while(True):
        creat_ac = int(input('signup?: '))
        account = input('account: ')            #Get account
        password = input('password: ')          #Get password
        user = AccountManage(account, password) 
        
        if(creat_ac):

            username = input('username: ')
            
            if_suc_signup = user.signup(username)
            
            if(if_suc_signup):
                print('You did it')             #return signup success
            else:
                print('rrrrr')                  #return signup fail
        
        else:
            if_suc_signin = user.signin()
            
            if(if_suc_signin):
                print('Wellcome')               #return signin success
            else:
                print('Wrong')                  #return signin fail