from tkinter import *
from tkinter import ttk
import threading
import string
import random
import time
from time import sleep
from threading import Thread

Main_Frame = Tk()
Main_Frame.title("SMS Simulator")
Main_Frame.geometry('600x600')

def producer():    # Produces nm number of messages 
    # using random.choices()
    # generating random strings
    global nm
    nm = Num_of_Messages.get()
    if len(nm)>0:
        nm=nm
    else:
        nm=1000    
    global l
    l=[]
    for i in range(int(nm)):
        N  = random.randint(1,100)
        res = ''.join(random.choices(string.ascii_uppercase +
        string.digits + string.ascii_lowercase, k=N))
       
        l.append(res)
    print(l)
    return l

Num_of_Messages = Entry()
Num_of_Messages.insert(0, "Enter No of Messages")
Num_of_Messages.pack(pady=30)
Failure_rate = Entry()
Failure_rate.insert(0, "Failure Rate")
Failure_rate.pack(pady=20)
Mean = Entry()
Mean.insert(0, "Mean")
Mean.pack(pady=20)
Refresh_Time = Entry()
Refresh_Time.insert(0, "Refresh time")
Refresh_Time.pack(pady=20)

Button(
    Main_Frame,
    text="Enter number of Messages", 
    padx=5, 
    pady=5,
    command=producer
    ).pack()

success_count=0
failure_count=0  
time_per_message=0

def sender(): # Takes messages from producer and sends it based on configurable mean and failure rate
    global failure_rate
    failure_rate= float(Failure_rate.get())
    failure_list = random.sample(l, round(failure_rate*len(l))) # 2 is number of messages failed
    print("failure_list: ",failure_list)
    success_list = []
    for element in l:
        if element not in failure_list:
            success_list.append(element)
    print("success_list",success_list)
    global mean
    mean=int(Mean.get())
    #mean =5
    x = mean*5
    global result
    result=[]
    for i in range(200):
        while True:
            samples = random.sample(range(1,(mean*2)+1), 5)
            #result=result+samples
            if sum(samples) == x:
                result=result+samples
                break  
    global success_count
    success_count=0
    global failure_count
    failure_count=0
    global time_per_message
    time_per_message=0    
    for j in range(len(l)):        
        if l[j] not in failure_list:
            time.sleep(result[j])
            print("Message sent: ",l[j])
            success_count=1+success_count
            print("success_count: ", success_count)
            time_per_message=time_per_message+ result[j]
            print("time_per_message: ", time_per_message)
        else:
            time.sleep(result[j])
            print("Message failed",l[j])
            failure_count=1+failure_count
            print("failure_count: ", failure_count)
            time_per_message=time_per_message+ result[j]
            print("time_per_message: ", time_per_message)    

def Progress_Monitor(): # Displays the parameters and updates it every N seconds 
    frame=Frame(Main_Frame,width=100,height=100,relief='solid',bd=1)
    frame.place(x=10,y=10)
    text=Label(frame,text="Sent Messages: "+str(success_count))
    text.pack()
    text1=Label(frame,text="Failed Messages: " + str(failure_count))
    text1.pack()
    if success_count+failure_count>0:
        Avg_time=round(time_per_message/(success_count+failure_count),1)
        text2=Label(frame,text="Avg Time per message: " + str(Avg_time))
        text2.pack()
    else: 
        text2=Label(frame,text="Avg Time per message: " + str(0))
        text2.pack()
        
def Refresher(): #Refreshes every n seconds
    Progress_Monitor()
    global n
    n=int(Refresh_Time.get())
    threading.Timer(n, Refresher).start()
  
def submit():
    if __name__ == '__main__':
        a = Thread(target = sender)
        b = Thread(target = Refresher)
        a.start()
        b.start()
    
submit_button = Button(Main_Frame, text="Submit", command= submit)

submit_button.pack(pady=20)
 
Main_Frame.mainloop()