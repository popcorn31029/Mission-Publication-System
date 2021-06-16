import socket
import tkinter as tk
import tkinter.font as tkFont
import threading
import time
from tkinter import ttk


HOST="127.0.0.1"
PORT=8000
DISCONNECT_MESSAGE="disconnect"
ADDR=(HOST,PORT)

clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # <===================建立socket  
clientsocket.connect(ADDR)
is_connect=1

lobbychoose=1 # 0=lobby 1=delegate 2=pickup  
username="username"
m_list=["aaa","bbb","ccc","ccc","ccc","ccc","ccc","ccc","ccc","ccc"]

name="username"
missionname="missionname"
destination="destination"
deadline="deadline"
salary="salary"
content="content"+'\n'+"hahah"

like_hate=0
likenum="+50"
hatenum="-60"

def listenthread():
    global m_list,name,missionname,destination,deadline,salary,content,clientsocket
    global lobbychoose,errormsg
    global username,likenum,hatenum
    global is_connect
    while True:
        try:
            x=clientsocket.recv(1024).decode('Big5') 
            x=x.split(" ")
            print(f"msg={x}")
            if x[0]=="account":
                if x[1]=="regist":  # 註冊
                    if x[2]=="success": # 成功
                        deletregistlayout()
                        setuserentrylayout() # 註冊畫面 => 大廳
                    elif x[2]=="fail": # 失敗
                        errormsg.place_forget()
                        errormsg=tk.Label(window,font="微軟正黑體 16 bold",bg="NavajoWhite",fg="red",text="regist fail!")
                        errormsg.place(x=180,y=520)
                elif x[1]=="signin": # 登入
                    if x[2]=="success": # 成功
                        username=x[3]
                        likenum="+"+str(abs(int(x[4])))
                        hatenum="-"+str(abs(int(x[5])))
                        deleteuserentrylayout()
                        setlobbychooselayout(0)  # 登入畫面 => 大廳
                    elif x[2]=="fail": # 失敗
                        errormsg.place_forget()
                        errormsg=tk.Label(window,font="微軟正黑體 16 bold",bg="NavajoWhite",fg="red",text="sign in fail!")
                        errormsg.place(x=180,y=520)
            elif x[0]=="mission":
                if x[1]=="search":  # 載入任務列表
                    m_list=[]
                    for i in range(2,len(x)):
                        m_list.append(x[i])
                    setmissionlist()
                elif x[1]=="detail": # 查看任務
                    name=x[3]
                    missionname=x[4]
                    destination=x[5]
                    deadline=x[6]
                    salary=x[7]
                    content=x[8].replace("_"," ")
                    content=content.replace("=",'\n')
                    delete_lobby_right()
                    deletelobbychooselayout()
                    if lobbychoose==0: # 接收任務 新增按鈕get
                        set_ready_pickup_layout()
                    elif lobbychoose==1: # 查看發布的任務 
                        if x[2]=="scorable":
                            set_already_delegate_layout(1)
                        else:
                            set_already_delegate_layout(0)
                    elif lobbychoose==2: # 查看接收的任務 新增按鈕complete 
                        set_already_pickup_layout()
                elif x[1]=="get":
                    if x[2]=="success":
                        ready_pickuptolobby()
                    elif x[2]=="fail":
                        errormsg.place_forget()
                        errormsg=tk.Label(window,font="微軟正黑體 16 bold",bg="NavajoWhite",fg="red",text="任務已被接取")
                        errormsg.place(x=450,y=660)
                elif x[1]=="complete":
                    already_pickuptolobby()
                elif x[1]=="score":
                    if x[2]=="success":
                        already_delegatetolobby()
        except Exception:
            break
    print("disconnect")
                


                


def deletemissionsample(): # 刪除樣板
    global mission_content_lb,mission_missionname_lb,mission_money_lb,mission_place_lb,mission_time_lb,mission_user_lb 
    global mission_canvas
    mission_content_lb.place_forget()
    mission_missionname_lb.place_forget()
    mission_money_lb.place_forget()
    mission_place_lb.place_forget()
    mission_time_lb.place_forget()
    mission_user_lb.place_forget()

    mission_canvas.place_forget()

def setmissionsample(): #任務樣板
    global mission_content_lb,mission_missionname_lb,mission_money_lb,mission_place_lb,mission_time_lb,mission_user_lb 
    global mission_canvas
    mission_canvas=tk.Canvas(width=600,height=700,bg="NavajoWhite")
    mission_canvas.place(x=0,y=0)

    mission_user_lb=tk.Label(window,font="微軟正黑體 16 bold",bg="NavajoWhite",text="發佈人:")
    mission_user_lb.place(x=20,y=70)
    mission_missionname_lb=tk.Label(window,font="微軟正黑體 16 bold",bg="NavajoWhite",text="任務名稱:")
    mission_missionname_lb.place(x=20,y=120)
    mission_place_lb=tk.Label(window,font="微軟正黑體 16 bold",bg="NavajoWhite",text="任務地點:")
    mission_place_lb.place(x=20,y=170)
    mission_time_lb=tk.Label(window,font="微軟正黑體 16 bold",bg="NavajoWhite",text="時間:")
    mission_time_lb.place(x=20,y=220)
    mission_money_lb=tk.Label(window,font="微軟正黑體 16 bold",bg="NavajoWhite",text="酬勞:")
    mission_money_lb.place(x=20,y=270)
    mission_content_lb=tk.Label(window,font="微軟正黑體 16 bold",bg="NavajoWhite",text="任務內容:")
    mission_content_lb.place(x=20,y=320)


def setmissioninfo(): # 顯示任務詳細資訊
    global missioninfo_content_lb,missioninfo_missionname_lb,missioninfo_money_lb,missioninfo_place_lb,missioninfo_time_lb,missioninfo_user_lb 
    global name,missionname,destination,deadline,salary,content
    missioninfo_user_lb=tk.Label(window,font="微軟正黑體 16 bold",bg="NavajoWhite",text=name)
    missioninfo_user_lb.place(x=130,y=70)
    missioninfo_missionname_lb=tk.Label(window,font="微軟正黑體 16 bold",bg="NavajoWhite",text=missionname)
    missioninfo_missionname_lb.place(x=130,y=120)
    missioninfo_place_lb=tk.Label(window,font="微軟正黑體 16 bold",bg="NavajoWhite",text=destination)
    missioninfo_place_lb.place(x=130,y=170)
    missioninfo_time_lb=tk.Label(window,font="微軟正黑體 16 bold",bg="NavajoWhite",text=deadline)
    missioninfo_time_lb.place(x=130,y=220)
    missioninfo_money_lb=tk.Label(window,font="微軟正黑體 16 bold",bg="NavajoWhite",text=salary)
    missioninfo_money_lb.place(x=130,y=270)
    missioninfo_content_lb=tk.Label(window,font="微軟正黑體 16 bold",justify="left",bg="NavajoWhite",text=content)
    missioninfo_content_lb.place(x=20,y=370)

def deletemissioninfo(): # 刪除任務資訊
    global missioninfo_missionname_lb,missioninfo_money_lb,missioninfo_place_lb,missioninfo_time_lb,missioninfo_user_lb 
    missioninfo_missionname_lb.place_forget()
    missioninfo_money_lb.place_forget()
    missioninfo_place_lb.place_forget()
    missioninfo_time_lb.place_forget()
    missioninfo_user_lb .place_forget()




def already_pickuptolobby(): # 已經接的任務 => 大廳(已經接的任務列表)
    delete_already_pickup_layout()
    setlobbychooselayout(2)

def delete_already_pickup_layout(): # 刪除已經接取任務介面
    global already_pickup_backbt,already_pickup_completebt
    deletemissionsample()
    deletemissioninfo()

    already_pickup_completebt.place_forget()
    already_pickup_backbt.place_forget()


def set_already_pickup_layout(): # 已經接取任務的資訊的介面
    global already_pickup_backbt,already_pickup_backimg,already_pickup_completebt,already_pickup_completeimg
    setmissionsample() #任務樣板
    setmissioninfo() # 任務資訊

    already_pickup_backimg=tk.PhotoImage(file="image/back.png")
    already_pickup_backbt=tk.Button(window,image=already_pickup_backimg,relief="flat",bd=0,width=100,height=50,command=already_pickuptolobby)
    already_pickup_backbt.place(x=18,y=15)

    already_pickup_completeimg=tk.PhotoImage(file="image/mission_completeimg.png")
    already_pickup_completebt=tk.Button(window,image=already_pickup_completeimg,relief="flat",bd=0,width=240,height=45,command=mission_complete)
    already_pickup_completebt.place(x=175,y=650)


def already_delegatetolobby(): # 已經發的任務 => 大廳(已經發的任務列表)
    delete_already_delegate_layout()
    setlobbychooselayout(1)

def delete_already_delegate_layout(): # 刪除已經發布任務介面
    global already_delegate_backbt,already_delegate_likebt,already_delegate_hatebt,already_delegate_scorebt
    deletemissionsample()
    deletemissioninfo()
    already_delegate_backbt.place_forget()
    already_delegate_likebt.place_forget()
    already_delegate_scorebt.place_forget()
    already_delegate_hatebt.place_forget()

def mission_complete(): # 完成任務
    global missionname,clientsocket
    msg="mission complete "+missionname
    print("client -> server: "+msg)
    clientsocket.send(msg.encode("Big5"))

def like():
    global already_delegate_likeimg,already_delegate_likebt,already_delegate_hatebt,already_delegate_hateimg
    global like_hate

    already_delegate_likeimg=tk.PhotoImage(file="image/like_greenimg.png")
    already_delegate_likebt["image"]=already_delegate_likeimg

    already_delegate_hateimg=tk.PhotoImage(file="image/hate_blackimg.png")
    already_delegate_hatebt["image"]=already_delegate_hateimg

    like_hate=1

def hate():
    global already_delegate_likeimg,already_delegate_likebt,already_delegate_hatebt,already_delegate_hateimg
    global like_hate

    already_delegate_likeimg=tk.PhotoImage(file="image/like_blackimg.png")
    already_delegate_likebt["image"]=already_delegate_likeimg

    already_delegate_hateimg=tk.PhotoImage(file="image/hate_redimg.png")
    already_delegate_hatebt["image"]=already_delegate_hateimg

    like_hate=-1

def score():
    global errormsg,like_hate,missionname,clientsocket
    if like_hate==0:
        errormsg.place_forget()
        errormsg=tk.Label(window,font="微軟正黑體 16 bold",bg="NavajoWhite",fg="red",text="尚未評分")
        errormsg.place(x=460,y=630)
        return
    msg="mission score "+missionname+" "+str(like_hate)
    print(f"client -> server: "+msg)
    clientsocket.send(msg.encode("Big5"))
    # already_delegatetolobby()

def set_already_delegate_layout(scorable): # 已經發布任務的資訊的介面
    global already_delegate_backbt,already_delegate_backimg,already_delegate_likeimg,already_delegate_likebt,already_delegate_hatebt,already_delegate_hateimg
    global already_delegate_scorebt,already_delegate_scoreimg,like_hate
    
    setmissionsample() #任務樣板
    setmissioninfo() # 任務資訊

    already_delegate_backimg=tk.PhotoImage(file="image/back.png")
    already_delegate_backbt=tk.Button(window,image=already_delegate_backimg,relief="flat",bd=0,width=100,height=50,command=already_delegatetolobby)
    already_delegate_backbt.place(x=18,y=15)

    if scorable==0:
        return
        
    like_hate=0
    already_delegate_likeimg=tk.PhotoImage(file="image/like_blackimg.png") # 讚
    already_delegate_likebt=tk.Button(window,image=already_delegate_likeimg,relief="flat",bd=0,width=85,height=85,command=like)
    already_delegate_likebt.place(x=220,y=520)

    already_delegate_hateimg=tk.PhotoImage(file="image/hate_blackimg.png") # 倒讚
    already_delegate_hatebt=tk.Button(window,image=already_delegate_hateimg,relief="flat",bd=0,width=85,height=85,command=hate)
    already_delegate_hatebt.place(x=320,y=520)

    already_delegate_scoreimg=tk.PhotoImage(file="image/scoreimg.png") # 評分按鈕
    already_delegate_scorebt=tk.Button(window,image=already_delegate_scoreimg,relief="flat",bd=0,width=150,height=40,command=score)
    already_delegate_scorebt.place(x=240,y=620)



def ready_pickuptolobby(): # 準備接任務 => 大廳
    delete_ready_pickup_layout()
    setlobbychooselayout(0)


def mission_get(): # 接取任務
    global missionname,name,errormsg,username,clientsocket
    if name==username:
        errormsg.place_forget()
        errormsg=tk.Label(window,font="微軟正黑體 16 bold",bg="NavajoWhite",fg="red",text="無法接取")
        errormsg.place(x=460,y=660)
        return 
    msg="mission get "+missionname
    print("client -> server: "+msg)
    clientsocket.send(msg.encode('Big5'))
    # ready_pickuptolobby()

def set_ready_pickup_layout(): # 建立 使用者準備接任務 介面
    global ready_pickup_backbt,ready_pickup_backimg,ready_pickup_pickupbt,ready_pickup_pickupimg
    setmissionsample() #任務樣板
    setmissioninfo() # 任務資訊

    ready_pickup_backimg=tk.PhotoImage(file="image/back.png")
    ready_pickup_backbt=tk.Button(window,image=ready_pickup_backimg,relief="flat",bd=0,width=100,height=50,command=ready_pickuptolobby)
    ready_pickup_backbt.place(x=18,y=15)

    ready_pickup_pickupimg=tk.PhotoImage(file="image/pickupimg.png")
    ready_pickup_pickupbt=tk.Button(window,image=ready_pickup_pickupimg,relief="flat",bd=0,width=240,height=50,command=mission_get)
    ready_pickup_pickupbt.place(x=175,y=650)



def delete_ready_pickup_layout():# 刪除 使用者準備接任務 介面
    global ready_pickup_backbt,ready_pickup_pickupbt
    deletemissionsample()
    deletemissioninfo()
    ready_pickup_backbt.place_forget()
    ready_pickup_pickupbt.place_forget()




def sendmission(): #使用者發布任務
    ## 送資料到server
    global user_delegate_missionname,user_delegate_money,user_delegate_place,user_delegate_time,errormsg,clientsocket
    flag=False
    user_delegate_content=user_delegate_content_text.get(1.0, tk.END+"-1c")
    user_delegate_content=user_delegate_content.replace(" ","_")
    user_delegate_content=user_delegate_content.replace('\n',"=")
    errormsg.place_forget()
    errormsg=tk.Label(window,bg="NavajoWhite",fg="red",text="can not be empty!")
    if user_delegate_missionname.get()=="":
        errormsg.place(x=480,y=127)
        flag=True
    elif user_delegate_place.get()=="":
        errormsg.place(x=480,y=177)
        flag=True
    elif user_delegate_time.get()=="":
        errormsg.place(x=480,y=227)
        flag=True
    elif user_delegate_money.get()=="":
        errormsg.place(x=480,y=283)
        flag=True
    elif user_delegate_content=="":
        errormsg.place(x=125,y=322)
        flag=True

    if flag==True: # 資料不完整
        return 
    msg="mission create "+user_delegate_missionname.get()+" "+user_delegate_place.get()+" "+user_delegate_time.get()+" "+user_delegate_money.get()+" "+user_delegate_content
    clientsocket.send(msg.encode('Big5'))
    print("client -> server: "+msg)
    delegatetolobby()

def delegatetolobby(): # 發布任務介面返回大聽
    delete_user_delegate_layout()
    setlobbychooselayout(0)

def delete_user_delegate_layout(): # 刪除發布任務介面
    # global user_delegate_content_lb,user_delegate_missionname_lb,user_delegate_money_lb,user_delegate_place_lb,user_delegate_time_lb,user_delegate_user_lb   
    global user_delegate_content_text,user_delegate_missionname_entry,user_delegate_money_entry,user_delegate_place_entry,user_delegate_time_entry
    global user_delegate_content,user_delegate_missionname,user_delegate_money,user_delegate_place,user_delegate_time
    global user_delegate_canvas,username,user_delegate_backimg,userdelegate_backbt,userdelegate_sendbt
    global user_delegate_user_lb

    user_delegate_content.set("")
    user_delegate_missionname.set("")
    user_delegate_money.set("")
    user_delegate_place.set("")
    user_delegate_time.set("")

    deletemissionsample()
    user_delegate_user_lb.place_forget()
    # user_delegate_content_lb.place_forget()
    # user_delegate_missionname_lb.place_forget()
    # user_delegate_money_lb.place_forget()
    # user_delegate_place_lb.place_forget()
    # user_delegate_time_lb.place_forget()

    user_delegate_content_text.place_forget()
    user_delegate_missionname_entry.place_forget()
    user_delegate_money_entry.place_forget()
    user_delegate_place_entry.place_forget()
    user_delegate_time_entry.place_forget()

    userdelegate_backbt.place_forget()
    # user_delegate_canvas.place_forget()
    userdelegate_sendbt.place_forget()


def set_user_delegate_layout(): # 建立發布任務介面
    # global user_delegate_content_lb,user_delegate_missionname_lb,user_delegate_money_lb,user_delegate_place_lb,user_delegate_time_lb,   
    global user_delegate_user_lb
    global user_delegate_content_text,user_delegate_missionname_entry,user_delegate_money_entry,user_delegate_place_entry,user_delegate_time_entry
    global user_delegate_content,user_delegate_missionname,user_delegate_money,user_delegate_place,user_delegate_time
    global user_delegate_canvas,username,user_delegate_backimg,userdelegate_backbt,userdelegate_sendbt,user_delegate_sendimg
    # user_delegate_canvas=tk.Canvas(width=600,height=700,bg="NavajoWhite")
    # user_delegate_canvas.place(x=0,y=0)

    
    # user_delegate_missionname_lb=tk.Label(window,font="微軟正黑體 16 bold",bg="NavajoWhite",text="任務名稱:")
    # user_delegate_missionname_lb.place(x=20,y=120)
    # user_delegate_place_lb=tk.Label(window,font="微軟正黑體 16 bold",bg="NavajoWhite",text="任務地點:")
    # user_delegate_place_lb.place(x=20,y=170)
    # user_delegate_time_lb=tk.Label(window,font="微軟正黑體 16 bold",bg="NavajoWhite",text="時間:")
    # user_delegate_time_lb.place(x=20,y=220)
    # user_delegate_money_lb=tk.Label(window,font="微軟正黑體 16 bold",bg="NavajoWhite",text="酬勞:")
    # user_delegate_money_lb.place(x=20,y=270)
    # user_delegate_content_lb=tk.Label(window,font="微軟正黑體 16 bold",bg="NavajoWhite",text="任務內容:")
    # user_delegate_content_lb.place(x=20,y=320)

    setmissionsample()

    user_delegate_user_lb=tk.Label(window,font="微軟正黑體 16 bold",bg="NavajoWhite",text=username)
    user_delegate_user_lb.place(x=130,y=70)

    user_delegate_missionname_entry=tk.Entry(window,font="微軟正黑體 16 bold",bd=1,width=25,textvariable=user_delegate_missionname)
    user_delegate_missionname_entry.place(x=130,y=125)
    user_delegate_place_entry=tk.Entry(window,font="微軟正黑體 16 bold",bd=1,width=25,textvariable=user_delegate_place)
    user_delegate_place_entry.place(x=130,y=175)
    user_delegate_time_entry=tk.Entry(window,font="微軟正黑體 16 bold",bd=1,width=25,textvariable=user_delegate_time)
    user_delegate_time_entry.place(x=130,y=225)
    user_delegate_money_entry=tk.Entry(window,font="微軟正黑體 16 bold",bd=1,width=25,textvariable=user_delegate_money)
    user_delegate_money_entry.place(x=130,y=275)
    user_delegate_content_text=tk.Text(window,font="微軟正黑體 16 bold",bd=1,width=40,height=10)
    user_delegate_content_text.place(x=20,y=370)

    user_delegate_backimg=tk.PhotoImage(file="image/back.png")
    userdelegate_backbt=tk.Button(window,image=user_delegate_backimg,relief="flat",bd=0,width=100,height=50,command=delegatetolobby)
    userdelegate_backbt.place(x=18,y=15)

    user_delegate_sendimg=tk.PhotoImage(file="image/user_delegate_sendimg.png")
    userdelegate_sendbt=tk.Button(window,image=user_delegate_sendimg,relief="flat",bd=0,width=240,height=50,command=sendmission)
    userdelegate_sendbt.place(x=175,y=650)

def delegating(): # 使用者發布任務
    delete_lobby_right()
    deletelobbychooselayout()
    set_user_delegate_layout()


def init_lobby_choose_color(): # 大廳左邊選擇欄初始白色
    global lobby_choose_lobbyimg,lobby_choose_lobbybt,lobby_choose_delegateimg,lobby_choose_delegatebt,lobby_choose_pickupimg,lobby_choose_pickupbt
    lobby_choose_lobbyimg=tk.PhotoImage(file="image/lobby_choose_lobbyimg.png")
    lobby_choose_lobbybt["image"]=lobby_choose_lobbyimg

    lobby_choose_delegateimg=tk.PhotoImage(file="image/lobby_choose_delegateimg.png")
    lobby_choose_delegatebt["image"]=lobby_choose_delegateimg

    lobby_choose_pickupimg=tk.PhotoImage(file="image/lobby_choose_pickupimg.png")
    lobby_choose_pickupbt["image"]=lobby_choose_pickupimg

def delete_lobby_right(): #刪除大廳右側的layout
    global lobbychoose
    if lobbychoose==0:
        deletelobby()
    elif lobbychoose==1:
        deletedelegate()
    elif lobbychoose==2:
        deletepickup()

def lobbyexit(): # 離開 回到登入介面
    global is_connect,clientsocket
    is_connect=0
    clientsocket.close()
    delete_lobby_right()
    deletelobbychooselayout()
    setuserentrylayout()


def refresh(): # 刷新任務
    global lobbychoose,clientsocket
    msg=""
    if lobbychoose==0:
        msg="mission search all"
    elif lobbychoose==1:
        msg="mission search post"
    elif lobbychoose==2:
        msg="mission search get"

    # delmissionlist()
    clientsocket.send(msg.encode('Big5'))
    print(f"client -> server: {msg}")

def deletepickup(): # 刪除接收的任務介面
    global pickup_canvas,pickup_title_label,refreshbt
    refreshbt.place_forget()
    pickup_canvas.place_forget()
    pickup_title_label.place_forget()
    delmissionlist()

def createpickup(): # 設置接收的任務介面
    global lobbychoose,lobby_choose_pickupimg,lobby_choose_pickupbt,refreshbt,refreshimg
    global pickup_canvas,pickup_title_label
    if lobbychoose==2:
        return

    delete_lobby_right()
    lobbychoose=2
    init_lobby_choose_color()

    # 改變選擇欄顏色
    lobby_choose_pickupimg=tk.PhotoImage(file="image/lobby_choose_pickupimg_red.png")
    lobby_choose_pickupbt["image"]=lobby_choose_pickupimg

    # 設置接收的任務介面

    pickup_canvas=tk.Canvas(width=400,height=700,bg="gainsboro")
    pickup_canvas.place(x=200,y=0)

    pickup_title_label=tk.Label(window,font="微軟正黑體 16 bold",relief="ridge",bd=2,width=31,height=4,fg="white",bg="cornflowerblue",text="接收的任務")
    pickup_title_label.place(x=200,y=0)

    refreshimg=tk.PhotoImage(file="image/refreshimg.png")
    refreshbt=tk.Button(window,image=refreshimg,relief="flat",bd=0,width=47,height=42,command=refresh)
    refreshbt.place(x=520,y=30)

    loadmission()  #載入任務
    # setmissionlist()
    

def deletedelegate(): #刪除發布的任務介面
    global delegate_canvas,delegate_title_label,refreshbt
    refreshbt.place_forget()
    delegate_canvas.place_forget()
    delegate_title_label.place_forget()
    delmissionlist()

def createdelegate(): # 設置發布的任務介面
    global lobbychoose,lobby_choose_delegateimg,lobby_choose_delegatebt,refreshbt,refreshimg
    global delegate_canvas,delegate_title_label
    if lobbychoose==1:
        return
   
    delete_lobby_right() 
    init_lobby_choose_color()
    lobbychoose=1   

    # 改變選擇欄顏色
    init_lobby_choose_color()
    lobby_choose_delegateimg=tk.PhotoImage(file="image/lobby_choose_delegateimg_red.png")
    lobby_choose_delegatebt["image"]=lobby_choose_delegateimg

    # 設置發布的任務介面
    delegate_canvas=tk.Canvas(width=400,height=700,bg="gainsboro")
    delegate_canvas.place(x=200,y=0)

    delegate_title_label=tk.Label(window,font="微軟正黑體 16 bold",relief="ridge",bd=2,width=31,height=4,fg="white",bg="cornflowerblue",text="發布的任務")
    delegate_title_label.place(x=200,y=0)

    refreshimg=tk.PhotoImage(file="image/refreshimg.png")
    refreshbt=tk.Button(window,image=refreshimg,relief="flat",bd=0,width=47,height=42,command=refresh)
    refreshbt.place(x=520,y=30)

    loadmission()  #載入任務
    # setmissionlist()

def missiondetail(name): # 查看任務
    global clientsocket
    msg="mission detail "+name
    # delete_lobby_right()
    # deletelobbychooselayout()
    # if lobbychoose==0: # 接收任務
    #     set_ready_pickup_layout()
    # elif lobbychoose==1: # 查看發布的任務 新增按鈕complete 若已經complete 設enable=false
    #     set_already_delegate_layout()
    # elif lobbychoose==2: # 查看接收的任務 新增狀態 complete incomplete
    #     set_already_pickup_layout()
    clientsocket.send(msg.encode('Big5'))
    print("client -> server: "+msg)


def addmission(): # 任務列表
    global m_list,missionframe2
    for i in range(len(m_list)):
        tk.Button(missionframe2,font="微軟正黑體 16 bold",activebackground="lightgrey",justify="left",text="任務名稱: "+m_list[i],width=29,height=5,command=lambda name=m_list[i]:missiondetail(name)).grid(row=i,column=0)

def myfunction(event): 
    global missioncanvas,lobbychoose
    if lobbychoose==0:
        missioncanvas.configure(scrollregion=missioncanvas.bbox("all"),width=380,height=520)
    else:
        missioncanvas.configure(scrollregion=missioncanvas.bbox("all"),width=380,height=620)
    
def on_mousewheel(event): # 控制滑鼠滾輪
    global missioncanvas
    scroll = -1 if event.delta > 0 else 1 
    missioncanvas.yview_scroll(scroll, "units") 

def setmissionlist(): #設置任務列表
    global missionlist,missionbar,missionframe,m_list,missioncanvas,missionframe2
    missionframe=tk.Frame(window,relief="flat",bd=1,bg="lightgrey",width=400,height=530)
    missionframe.place(x=200,y=100)
    
    missioncanvas=tk.Canvas(missionframe,bg="lightgrey")
    missionframe2=tk.Frame(missioncanvas,bg="lightgrey",width=400,height=530)
    missionbar=tk.Scrollbar(missionframe,orient="vertical",command=missioncanvas.yview)
    missioncanvas.configure(yscrollcommand=missionbar.set)

    missionbar.pack(side="right",fill="y")
    missioncanvas.pack(side="left")
    missioncanvas.create_window((0,0),window=missionframe2,anchor='nw')
    missionframe2.bind("<Configure>",myfunction)
    missioncanvas.bind_all("<MouseWheel>", on_mousewheel)
    addmission()

def delmissionlist():
    global missionlist,missionbar,missionframe,missionframe2
    missionframe.place_forget()

def loadmission(): # 載入任務
    global lobbychoose,clientsocket      # 根據不同的畫面 和server 要求不同的任務列表 
    msg=""
    if lobbychoose==0:
        msg="mission search all"
    elif lobbychoose==1:
        msg="mission search post"
    elif lobbychoose==2:
        msg="mission search get"
    
    print("client -> server: "+msg)
    # setmissionlist()
    clientsocket.send(msg.encode('Big5'))

def deletelobby(): # 刪除任務大廳介面
    global lobby_canvs,lobby_delegatebt,lobby_title_label,refreshbt,comboExample,lobby_keyword,lobby_keyword_bt,lobby_keyword_entry
    refreshbt.place_forget()
    lobby_canvs.place_forget()
    lobby_title_label.place_forget()
    lobby_delegatebt.place_forget()
    comboExample.place_forget()
    lobby_keyword.set("")
    lobby_keyword_bt.place_forget()
    lobby_keyword_entry.place_forget()
    delmissionlist()

def searchkeyword():
    global comboExample,lobby_keyword,clientsocket
    msg="mission search keyword "
    if comboExample.get()=="地點":
        msg+="destination "
    elif comboExample.get()=="名稱":
        msg+="missionname "
    elif comboExample.get()=="內容":
        msg+="content "
    msg+=lobby_keyword.get()
    print(msg)

def createlobby(): # 設置任務大廳介面
    global lobby_choose_lobbyimg,lobbychoose,lobby_choose_lobbybt,refreshbt,refreshimg
    global lobby_canvs,lobby_delegatebt,lobby_title_label,comboExample,lobby_keyword,lobby_keyword_bt,lobby_keyword_entry
    if lobbychoose==0:
        return

    delete_lobby_right()
    init_lobby_choose_color()
    lobbychoose=0

    # 改變選擇欄顏色
    lobby_choose_lobbyimg=tk.PhotoImage(file="image/lobby_choose_lobbyimg_red.png")
    lobby_choose_lobbybt["image"]=lobby_choose_lobbyimg

    # 設置大廳
    lobby_canvs=tk.Canvas(width=400,height=700,bg="gainsboro")
    lobby_canvs.place(x=200,y=0)



    lobby_delegatebt=tk.Button(window,font="微軟正黑體 16 bold",relief="ridge",bd=2,width=30,height=2,activebackground="chocolate",activeforeground="white",fg="white",bg="sandybrown",text="發布任務",command=delegating)
    lobby_delegatebt.place(x=200,y=627)

    lobby_title_label=tk.Label(window,font="微軟正黑體 16 bold",relief="ridge",bd=2,width=31,height=4,fg="white",bg="cornflowerblue",text="任務大廳")
    lobby_title_label.place(x=200,y=0)
    
    refreshimg=tk.PhotoImage(file="image/refreshimg.png")
    refreshbt=tk.Button(window,image=refreshimg,relief="flat",bd=0,width=47,height=42,command=refresh)
    refreshbt.place(x=520,y=30)

    comboExample = ttk.Combobox(window, 
        values=[
            "名稱", 
            "地點",
            "內容"
        ]
        ,width=4
    )
    comboExample.place(x=260,y=70)
    lobby_keyword_entry=tk.Entry(window,width=20,textvariable=lobby_keyword)
    lobby_keyword_entry.place(x=320,y=73)
    lobby_keyword_bt=tk.Button(window,text="搜尋",command=searchkeyword)
    lobby_keyword_bt.place(x=480,y=70)

    loadmission()  #載入任務
    # setmissionlist()

def deletelobbychooselayout(): # 清除大廳左邊選擇欄
    global lobby_choose_canvas,lobby_choose_delegatebt,lobby_choose_exit,lobby_choose_lobbybt,lobby_choose_pickupbt
    lobby_choose_canvas.place_forget()
    lobby_choose_delegatebt.place_forget()
    lobby_choose_exit.place_forget()
    lobby_choose_lobbybt.place_forget()
    lobby_choose_pickupbt.place_forget()

def setlobbychooselayout(number):  # 設置大廳左邊選擇欄
    global lobby_choose_canvas,lobby_choose_delegatebt,lobby_choose_exit,lobby_choose_lobbybt,lobby_choose_pickupbt,lobby_choose_pickupimg,lobby_choose_lobbyimg,lobby_choose_exitimg,lobby_choose_delegateimg
    global lobbychoose,lobby_choose_username,username,iconimg
    global lobby_choose_hate,lobby_choose_like,lobby_choose_seperate,likenum,hatenum

    lobby_choose_canvas=tk.Canvas(width=200,height=700,bg="seagreen")
    lobby_choose_canvas.place(x=0,y=0)

    iconimg=tk.PhotoImage(file="image/iconimg.png")
    lobby_choose_canvas.create_image(100,75,image=iconimg)

    lobby_choose_like=tk.Label(window,font="微軟正黑體 20 bold",fg="springgreen",bg="seagreen",width=3,text=likenum)
    lobby_choose_like.place(x=30,y=170)

    lobby_choose_hate=tk.Label(window,font="微軟正黑體 20 bold",fg="red",bg="seagreen",width=3,text=hatenum)
    lobby_choose_hate.place(x=110,y=170)

    lobby_choose_seperate=tk.Label(window,font="微軟正黑體 20 bold",fg="black",bg="seagreen",width=1,text="/")
    lobby_choose_seperate.place(x=90,y=170)

    lobby_choose_username=tk.Label(window,font="微軟正黑體 16 bold",bg="yellow",width=15,text=username)
    lobby_choose_username.place(x=0,y=255)

    init_lobby_choose_color()
    lobbychoose=-1
    if number==0:
        createlobby()
    elif number==1:
        createdelegate()
    elif number==2:
        createpickup()

    # lobby_choose_lobbyimg=tk.PhotoImage(file="image/lobby_choose_lobbyimg_red.png")
    lobby_choose_lobbybt=tk.Button(window,image=lobby_choose_lobbyimg,bd=0,width=200,height=100,command=createlobby)
    lobby_choose_lobbybt.place(x=0,y=300)

    # lobby_choose_delegateimg=tk.PhotoImage(file="image/lobby_choose_delegateimg.png")
    lobby_choose_delegatebt=tk.Button(window,image=lobby_choose_delegateimg,bd=0,width=200,height=100,command=createdelegate)
    lobby_choose_delegatebt.place(x=0,y=400)

    # lobby_choose_pickupimg=tk.PhotoImage(file="image/lobby_choose_pickupimg.png")
    lobby_choose_pickupbt=tk.Button(window,image=lobby_choose_pickupimg,bd=0,width=200,height=100,command=createpickup)
    lobby_choose_pickupbt.place(x=0,y=500)

    lobby_choose_exitimg=tk.PhotoImage(file="image/lobby_choose_exitimg.png")
    lobby_choose_exit=tk.Button(window,image=lobby_choose_exitimg,bd=0,width=200,height=100,command=lobbyexit)
    lobby_choose_exit.place(x=0,y=600)



def registback(): # 返回登入畫面    
    deletregistlayout()
    setuserentrylayout()

def regist(): #註冊
    global registname,registpass,registuser,errormsg,clientsocket
    errormsg.place_forget()
    errormsg=tk.Label(window,bg="NavajoWhite",fg="red",text="can not be empty!")
    if registuser.get()=="":
        errormsg.place(x=470,y=260)
    elif registname.get()=="":
        errormsg.place(x=470,y=330)
    elif registpass.get()=="":
        errormsg.place(x=470,y=410)
    else:
        msg="account regist "+registname.get()+" "+registpass.get()+" "+registuser.get()
        # deletregistlayout()
        # setuserentrylayout()
        # print("client -> server: "+msg)
        clientsocket.send(msg.encode('Big5'))                  # <========================= 向server 傳遞註冊資料

def deletregistlayout(): #清除註冊介面
    global registcanvas,registnameentry,registpassentry,registbackbutton,registbutton,registname,registpass,registuserentry,registuser
    registcanvas.place_forget()
    registnameentry.place_forget()
    registuserentry.place_forget()
    registpassentry.place_forget()
    registbackbutton.place_forget()
    registbutton.place_forget()

    registname.set("")
    registpass.set("")
    
    registuser.set("")

def setregistlayout(): # 設置註冊介面
    global registcanvas,registnameimg,registpassimg,registnameentry,registpassentry,registbackbutton,registbutton,registbackimg,registconfirmimg
    global registuserimg,registuserentry,registuser,registtitleimg

    registcanvas=tk.Canvas(width=600,height=700,bg="NavajoWhite")
    registcanvas.place(x=0,y=0)

    registtitleimg=tk.PhotoImage(file="image/registtitleimg.png")
    registcanvas.create_image(270,130,image=registtitleimg)

    registuserimg=tk.PhotoImage(file="image/registuserimg.png")
    registcanvas.create_image(128,270,image=registuserimg)
    registnameimg=tk.PhotoImage(file="image/userimg.png")
    registcanvas.create_image(128,345,image=registnameimg)
    registpassimg=tk.PhotoImage(file="image/passimg.png")
    registcanvas.create_image(130,420,image=registpassimg)

    registuserentry=tk.Entry(window,font="微軟正黑體 16 bold",bd=3,width=20,textvariable=registuser)
    registuserentry.place(x=190,y=255,height=30)
    registnameentry=tk.Entry(window,font="微軟正黑體 16 bold",bd=3,width=20,textvariable=registname)
    registnameentry.place(x=190,y=327,height=30)
    registpassentry=tk.Entry(window,font="微軟正黑體 16 bold",bd=3,width=20,textvariable=registpass)
    registpassentry.place(x=190,y=407,height=30)

    registbackimg=tk.PhotoImage(file="image/registbackimg.png")
    registbackbutton=tk.Button(window,image=registbackimg,relief="flat",bd=0,width=100,height=48,command = registback)
    registbackbutton.place(x=180,y=455)

    registconfirmimg=tk.PhotoImage(file="image/registconfirmimg.png")
    registbutton=tk.Button(window,image=registconfirmimg,relief="flat",bd=0,width=100,height=48,command = regist)
    registbutton.place(x=320,y=455)


def enter(): # 登入
    global entername,enterpass,errormsg,clientsocket
    errormsg.place_forget()
    errormsg=tk.Label(window,bg="NavajoWhite",fg="red",text="can not be empty!")
    if entername.get()=="":
        errormsg.place(x=470,y=330)
        # print("username cannt be empty!")
    elif enterpass.get()=="":
        errormsg.place(x=470,y=410)
        # print("password cannt be empty!")
    else:
        msg="account signin "+entername.get()+" "+enterpass.get()
        # setlobbychooselayout(0)
        # deleteuserentrylayout()
        # print("client -> server: "+msg)
        clientsocket.sendall(msg.encode('Big5'))   #<================================ 向server 傳遞登入資料

def enterregist(): # 進入註冊畫面
    deleteuserentrylayout()
    setregistlayout()


def setuserentrylayout(): # 設置登入介面
    global entry_canvas,entry_title_img,usrnameentrybutton,usrregistbutton,usrpassentry,usrnameentry,usrnameimg,usrpassimg,enterimg,registimg
    global is_connect,clientsocket
    entry_canvas=tk.Canvas(width=600,height=700,bg="NavajoWhite")
    entry_canvas.place(x=0,y=0)
    entry_title_img=tk.PhotoImage(file="image/titleimage.png")
    entry_canvas.create_image(300,150,image=entry_title_img)


    usrnameimg=tk.PhotoImage(file="image/userimg.png")
    entry_canvas.create_image(128,345,image=usrnameimg)
    usrpassimg=tk.PhotoImage(file="image/passimg.png")
    entry_canvas.create_image(130,420,image=usrpassimg)

    usrnameentry=tk.Entry(window,font="微軟正黑體 16 bold",bd=3,width=20,textvariable=entername)
    usrnameentry.place(x=190,y=327,height=30)
    usrpassentry=tk.Entry(window,font="微軟正黑體 16 bold",show='*',bd=3,width=20,textvariable=enterpass)
    usrpassentry.place(x=190,y=407,height=30)

    enterimg=tk.PhotoImage(file="image/enterimg.png")
    registimg=tk.PhotoImage(file="image/registimg.png")

    usrnameentrybutton=tk.Button(window,image=enterimg,relief="flat",bd=0,bg="NavajoWhite",highlightbackground="NavajoWhite",width=110,height=45,command = enter)
    usrnameentrybutton.place(x=180,y=455)
    usrregistbutton=tk.Button(window,image=registimg,relief="flat",bd=0,bg="NavajoWhite",highlightbackground="NavajoWhite",width=110,height=45,command = enterregist)
    usrregistbutton.place(x=310,y=453)

    if is_connect==0: # 斷線重連
        is_connect=1
        sockettmp=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        clientsocket=sockettmp
        clientsocket.connect(ADDR)
        thread = threading.Thread(target=listenthread) # 開啟thread 監聽server
        thread.start()
        

def deleteuserentrylayout(): # 清除登入介面
    global entry_canvas,usrnameentrybutton,usrregistbutton,usrpassentry,usrnameentry,entername,enterpass
    entry_canvas.place_forget()
    usrnameentrybutton.place_forget()
    usrregistbutton.place_forget()
    usrpassentry.place_forget()
    usrnameentry.place_forget()
    entername.set("")
    enterpass.set("")

window=tk.Tk()
window.geometry('600x700')
window.title("mission publication")

# 登入介面宣告
usrnameentry=tk.Entry()
usrpassentry=tk.Entry()
usrnameentrybutton=tk.Button()
usrregistbutton=tk.Button()
entry_canvas=tk.Canvas()
entry_title_img=tk.PhotoImage()
usrnameimg=tk.PhotoImage()
usrpassimg=tk.PhotoImage()
enterimg=tk.PhotoImage()
registimg=tk.PhotoImage()

entername=tk.StringVar()
enterpass=tk.StringVar()


# 錯誤訊息
errormsg=tk.Label()

#註冊介面宣告
registcanvas=tk.Canvas()
registtitleimg=tk.PhotoImage()
registnameimg=tk.PhotoImage()
registpassimg=tk.PhotoImage()
registuserimg=tk.PhotoImage()
registnameentry=tk.Entry()
registpassentry=tk.Entry()
registuserentry=tk.Entry()
registbackbutton=tk.Button()
registbutton=tk.Button()
registbackimg=tk.PhotoImage()
registconfirmimg=tk.PhotoImage()

registuser=tk.StringVar()
registname=tk.StringVar()
registpass=tk.StringVar()


#大廳選單宣告
lobby_choose_canvas=tk.Canvas()
lobby_choose_username=tk.Label()
lobby_choose_lobbybt=tk.Button()
lobby_choose_delegatebt=tk.Button()
lobby_choose_pickupbt=tk.Button()
lobby_choose_exit=tk.Button()
lobby_choose_like=tk.Label()
lobby_choose_hate=tk.Label()
lobby_choose_seperate=tk.Label

lobby_choose_lobbyimg=tk.PhotoImage()
lobby_choose_delegateimg=tk.PhotoImage()
lobby_choose_pickupimg=tk.PhotoImage()
lobby_choose_exitimg=tk.PhotoImage()

iconimg=tk.PhotoImage()

refreshbt=tk.Button()
refreshimg=tk.PhotoImage()

#大廳宣告
lobby_canvs=tk.Canvas()
lobby_delegatebt=tk.Button()
lobby_title_label=tk.Label()
missionframe=tk.Frame()
missionframe2=tk.Frame()
missionlist=tk.Listbox()
missionbar=tk.Scrollbar()
missioncanvas=tk.Canvas()

comboExample = ttk.Combobox()
lobby_keyword_entry=tk.Entry()
lobby_keyword=tk.StringVar()
lobby_keyword_bt=tk.Button()

#發布的任務宣告
delegate_canvas=tk.Canvas()
delegate_title_label=tk.Label()


#接收的任務宣告
pickup_canvas=tk.Canvas()
pickup_title_label=tk.Label()


#任務樣板宣告
mission_canvas=tk.Canvas()
mission_user_lb=tk.Label()
mission_missionname_lb=tk.Label()
mission_place_lb=tk.Label()
mission_time_lb=tk.Label()
mission_money_lb=tk.Label()
mission_content_lb=tk.Label()

#任務資訊宣告
missioninfo_user_lb=tk.Label()
missioninfo_missionname_lb=tk.Label()
missioninfo_place_lb=tk.Label()
missioninfo_time_lb=tk.Label()
missioninfo_money_lb=tk.Label()
missioninfo_content_lb=tk.Label()

#準備接取任務宣告
ready_pickup_backimg=tk.PhotoImage()
ready_pickup_backbt=tk.Button()
ready_pickup_pickupimg=tk.PhotoImage()
ready_pickup_pickupbt=tk.Button()

#已經發布任務介面宣告
already_delegate_backimg=tk.PhotoImage()
already_delegate_backbt=tk.Button()
already_delegate_completeimg=tk.PhotoImage()
already_delegate_completebt=tk.Button()
already_delegate_likebt=tk.Button()
already_delegate_hatebt=tk.Button()
already_delegate_scorebt=tk.Button()
already_delegate_likeimg=tk.PhotoImage()
already_delegate_hateimg=tk.PhotoImage()
already_delegate_scoreimg=tk.PhotoImage()


#已經接取任務介面宣告
already_pickup_backbt=tk.Button()
already_pickup_backimg=tk.PhotoImage()

#發布任務需告
user_delegate_user_entry=tk.Entry()
user_delegate_missionname_entry=tk.Entry()
user_delegate_place_entry=tk.Entry()
user_delegate_time_entry=tk.Entry()
user_delegate_money_entry=tk.Entry()
user_delegate_content_text=tk.Text()

user_delegate_missionname=tk.StringVar()
user_delegate_place=tk.StringVar()
user_delegate_time=tk.StringVar()
user_delegate_money=tk.StringVar()
user_delegate_content=tk.StringVar()

user_delegate_backimg=tk.PhotoImage()
userdelegate_backbt=tk.Button()
user_delegate_sendimg=tk.PhotoImage()
userdelegate_sendbt=tk.Button()

#進入登入介面
setuserentrylayout()

thread = threading.Thread(target=listenthread) # 開啟thread 監聽server
thread.start()

def onclose():
    # clientsocket.send(DISCONNECT_MESSAGE.encode())
    clientsocket.close()
    window.destroy()

window.protocol("WM_DELETE_WINDOW",onclose)
window.mainloop()