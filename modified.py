# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 18:04:15 2022

@author: Khaled
"""

import pyautogui as pt
import random 
from time import sleep
import pyperclip 
import pandas as pd
import numpy as np 

df = pd.read_excel("chatbot info.xls")
branch_number = df['Branch Number'].unique()

count = 0
columns = list(df.columns)

sleep(3)
while True:
    position1  = pt.locateOnScreen("smile_attach.png",confidence = 0.7)
    print("please open whatsapp")
    sleep(2)
    if position1 is not None:
        x = position1[0]
        y = position1[1]
        break


#Get message 
def get_msg():
    global x ,y 
    while True:
        position = pt.locateOnScreen("smile_attach.png",confidence = 0.7)
        if position is not None:
            x = position[0]
            y = position[1]
            break
    pt.moveTo(x,y)#,duration = 0.05)
    pt.moveTo(x+130,y-60)#,duration = 0.05)  # 160 -85
    pt.tripleClick()
    pt.rightClick()
    pt.moveRel(12,15)
    pt.click()
    whatsmsg = pyperclip.paste()
    pt.click()
    print("whatsapp message is: "+whatsmsg)
    return whatsmsg
    

#post 

def post_response(message):
    global x ,y 
    position = pt.locateOnScreen("smile_attach.png",confidence = 0.7)
    x = position[0]
    y = position[1]
    pt.moveTo(x+200,y+20)#,duration = 0.005)
    pt.click()
    msg_lst = message.split("#")
    for i in msg_lst:
        pt.typewrite(i,interval = 0.0001)
        # Holds down the alt key
        pt.keyDown("shift")
        # Presses the enter key once
        pt.typewrite('\n',interval = 0.0001)
        # Lets go of the alt key
        pt.keyUp("shift")
    pt.typewrite('\n',interval = 0.0001)
    
    
#welcoming    
def welcoming(msg):
    global x ,y 
    position = pt.locateOnScreen("smile_attach.png",confidence = 0.7)
    x = position[0]
    y = position[1]
    pt.moveTo(x+200,y+20,duration = 0.05)
    pyperclip.copy(msg)
    pt.hotkey("ctrl", "v")
    pt.typewrite('\n',interval = 0.0001)    
    pt.typewrite('\n',interval = 0.0001)
    
    
#processes the response
def process_response(msg):
    resp_msg = ''
    global count 
    if msg.isnumeric() and (count < 2):
        if msg.lower() in branch_number :
            indexes = np.where(df['Branch Number'].values == msg.lower())[0]
            for i in indexes:
                if(df.iloc[i]["STATUS"].lower() == "pending"):
                    for col in columns:
                        resp_msg =  resp_msg +str(col)+": "+ str(df.iloc[i][col])+"#"
                    resp_msg +='============================================\n'
        else:
            resp_msg = "please enter correct Branch number\n"
            count += 1
    elif msg.isnumeric() and (count == 2):
        resp_msg = "your branch number is not recorded "
        count += 1
    elif (msg.isnumeric() and (count > 2)) or count == 0:
        count = 0
        resp_msg = """Hi # Welcome to Supply logistics department bot # To display your current shipments please type your *branch Number *"""
    else:
        resp_msg = """Hi # Welcome to Supply logistics department bot # To display your current shipments please type your *branch Number *"""
    return resp_msg       


#check for white pixel 
def is_white(x_offset,y_offset):
    global x , y 
    count = 0
    flag = False
    pt.moveTo(x+x_offset+5,y+y_offset+5)
    if pt.pixelMatchesColor(int(x+x_offset+3), int(y+y_offset+3),(255,255,255),tolerance=10):
        count +=1
        
    pt.moveTo(x+x_offset+5,y+y_offset-5)
    if pt.pixelMatchesColor(int(x+x_offset+3), int(y+y_offset-3),(255,255,255),tolerance=10): 
        count +=1
        
    pt.moveTo(x+x_offset-5,y+y_offset+5)
    if pt.pixelMatchesColor(int(x+x_offset-3), int(y+y_offset+3),(255,255,255),tolerance=10):
        count +=1
        
    pt.moveTo(x+x_offset-5,y+y_offset-5)
    if pt.pixelMatchesColor(int(x+x_offset-3), int(y+y_offset-3),(255,255,255),tolerance=10): 
        count +=1
        
    if count >= 2:
        flag = True
    
    return flag 






#check for new messages
def check_for_new_messages():
    pt.moveTo(x+70,y-40)     #110 -30
    #continuously check for green dot and new messages
    while True:
        try:
            position = pt.locateOnScreen("greendot.png",confidence = 0.8)
            if position is not None:
                pt.moveTo(position)
                pt.moveRel(-100,0)
                pt.click()
                sleep(1)#4)
        except(Exception):
            print(" No new messages ")
        if is_white(70,-40):
            print("is_white")
            processed_message = process_response(get_msg())
            post_response(processed_message)
        else:
            print("No new message yet ...")
        sleep(4)
            
            
check_for_new_messages()
# processed_msg =  process_response(get_msg())


# post_response(processed_msg)







