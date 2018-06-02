
# coding: utf-8

#  # This Paint Application is simple, uses some math and cleverly uses loops!.
# 
# #### Run the application, a black window will pop up.
# 
# ##### Default brush is circle, and color is red(can be changed in code).
# ##### Press 'r' for rectange (orange), press 'e' for ellipse and press 'o' for circle.
# ##### Press 'c' to clear and 'esc' to exit.
# 

# # Adding many changes to this, adding a lot of features to paint tool.
# 
# ### Now this features a toggle help feature, that means you can see what you can do in paint by toggling 'HELP' on or off. 
# 
# ### Adding TrackBars to change color of the paint.
# 
# ### Adding Trackbar to change the size of the brush.
# 
# ### Adding escape button to switch off the paint application

# In[11]:


#self implementing paint application

import cv2
import numpy as np
import time 
import os

# delcaring global r g b values to pass color to the mouseCallBack Funtion
global r,g,b,Size
r=255
g=255
b=255 #so that (b,g,r) shows white
Size=3
drawing=True
# draw function to define what to do when mouse is clicked
def draw(event,x,y,flags,param):
    # this is a clever function in OpenCV
    
    #if mouse is clicked, then drawing is set to True and function returns.
    #if mouse is left idle, then drawing is false and the fuction returns
    # if the mouse is click + drag, then drawing is set to true and the drag function works from next iteration
    #while if the mouse was not clicked, or no drawing, then drag is not functional because of the If statement in the loop
    
    global drawing
    if event==cv2.EVENT_LBUTTONDOWN:
        drawing = True
        if toggle==0: # print circles
            cv2.circle(img,(x,y),Size,(b,g,r),-1)
        elif toggle==1:
            cv2.rectangle(img,(x-Size,y-Size),(x+Size,y+Size),(b,g,r),-1)
        else:
            cv2.ellipse(img,(x,y),(Size+10,Size+5),0,0,360,(b,g,r),-1)
    elif event==cv2.EVENT_MOUSEMOVE:
        if drawing==True:
            if toggle==0: # print circles
                cv2.circle(img,(x,y),Size,(b,g,r),-1)
            elif toggle== 1:
                cv2.rectangle(img,(x-Size,y-Size),(x+Size,y+Size),(b,g,r),-1)
            elif toggle==2:
                cv2.ellipse(img,(x,y),(Size+10,Size+5),0,0,360,(b,g,r),-1)
        else:
            return
    elif event==cv2.EVENT_LBUTTONUP:
        drawing = False


# In[12]:


def slideShow(myPath):
    myPath='G:\Programming\opencv\Paint_Application\Images'
    cv2.namedWindow('slideShow')
    directory='G:\Programming\opencv\Images'# check if these are correctly put slashes.
    #directory='G:\Programming\opencv\Paint_Application\Images'# check if these are correctly put slashes.

    fileNames=os.listdir(directory)
    i=1
    path=0
    #get a starting image outside the loop and get images from file 1 by one. When the images end,
    # the return value will help us terminate the loop(while(True)<<one )
    img1=cv2.imread('G:\Programming\opencv\Images\img2.jpg')
    flag=False
    i=1
    while(i<len(fileNames) and flag==False):
        flag1=0
        if fileNames[i].endswith(".jpg") or fileNames[i].endswith(".png") :
            path=os.path.join(directory,fileNames[i])

        else:
            i=i+1
            continue
        #img2=cv2.imread(myPath) # for testing
        img2=cv2.imread('G:\Programming\opencv\Images\img5.jpg')
        
        #img2=cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
        if not len(img1) or not len(img2):
            break
        for j in range(1,50):
            #print(img1.shape, img2.shape)
            img1= cv2.addWeighted(img1,1-j/100.0,img2,j/100.0,0)
            #img1=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
            cv2.imshow('slideShow',img1)
            k= cv2.waitKey(40) & 0xFF 
            if k==ord('a'): # initially there is very little change in image 1 so image stays static, then image 2 takes over and changes image 1. So the transition works very smothly.
                break # this is to speed through the pictures
            elif k==27:
                flag1=1
                break
        if flag1:
            break# add some delay show the image before switching to other image
        i=i+1

    cv2.destroyAllWindows()


# In[13]:


import os
img=np.zeros((640,480,3),np.uint8) #create an image that is black
cv2.namedWindow('image') #creates an openCv window
cv2.setMouseCallback('image',draw) # defines what a mouse click should do. So if mouse is clicked, then there is a function associated with that that click which is immediately executed
#'image' is not a string, but window name, draw function is auto given arguments as above^^^


def nothing(x):
    pass
#Lets create some trackbars for PaintTM:P 
cv2.namedWindow('paint_selector') #creates an openCv window

cv2.createTrackbar('R','paint_selector',255,255,nothing)
cv2.createTrackbar('G','paint_selector',255,255,nothing)
cv2.createTrackbar('B','paint_selector',255,255,nothing)# remember 0 is default value, not start range
cv2.createTrackbar('Size','paint_selector',3,20,nothing)


global toogle
callStack=[]
toggle=0
reset=False
Help=False
xx=0
start=time.time() # this is start time. Every 3 seconds or so, I will store the img, so that I can undo it:)
myPath='G:\Programming\opencv\Paint_Application\Images'
font = cv2.FONT_HERSHEY_SIMPLEX

while(1):
    
    cv2.imshow('image',img)
#     if(cv2.waitKey(10) & 0xFF==ord('m')):
#         toggle=bool(abs(int(toggle)-1))
    
    k= cv2.waitKey(1) & 0xFF
    #print(k)
    #these are the toggles. There is a catch, that k==27 has to be the ending statement and there must be no else statement only if and elif statement so that this code is stuck till the toggle is implemented.
    #if there was an else statement, then due to rapid refresh rate of the while loop(due to waitKey(1)), else will always execute, if otherwise you keep pressing a button!
    
    if k==ord('r'):
        toggle=1
    elif k==ord('e'):
        toggle=2
    elif k==ord('o') :
        toggle=0
    elif k==ord('c'):
        img=np.zeros((640,480,3),np.uint8) #create an image that is black
    elif k==ord('h'):
        Help=bool((Help-1)%2)
        img=np.zeros((640,480,3),np.uint8)
    elif k==ord('t'):
        callStack.append(img.copy())
        
    elif k==ord('y'):
        if(len(callStack)==0):
            continue;
        else:  
            # this updates the image using stack
            img=np.zeros((640,480,3),np.uint8)
            img=callStack.pop()
            
            
    elif k==ord('s'): # if I press s
        # save my work in images folder and sleep the execution for 3 seconds. print some message on the screen for those 3 seconds and then remove it!
        imageName='image_'
        extention='.jpg'
        fileCount=xx
        # so file name to be saved is:
        img1=img.copy()
        img=np.zeros((640,480,3),np.uint8)
        cv2.putText(img,'Saving your file, please wait...',(100,300), font, 1,(255,255,255),2,cv2.LINE_AA)
        cv2.imshow('image',img)
        time.sleep(3)  # sleeps the computer process for 3 seconds!
        img=img1.copy()
        cv2.imshow('image',img)
        imageName=imageName+str(fileCount)+extention
        cv2.imwrite(os.path.join(myPath,imageName),img)
        xx+=1
    elif k==ord('u'):
        # present the user with the slide show. Then exit
        slideShow(myPath)
        break
    elif k==27:# pressed escape
        break 
        
    end=time.time()
    #print(end-start)
    if (int(end-start)%60)==0:
        # 60 seconds have elapsed
        
        callStack.append(img.copy())
        time.sleep(1)
    #no else statement !!!
    #Getting the position from each trachbar ie the color from each thing.
    r = cv2.getTrackbarPos('R','paint_selector')
    g = cv2.getTrackbarPos('G','paint_selector')
    b = cv2.getTrackbarPos('B','paint_selector')
    Size=cv2.getTrackbarPos('Size','paint_selector')
    img1=img.copy()
    img1[:]=[b,g,r] # the track window's color will display the color of my brush:
    cv2.imshow('paint_selector',img1)
    if (Help==True):
        cv2.putText(img,'PaintTM',(170,570), font, 1,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(img,'PRESS *r* or *e* or *o* ',(80,600), font, 0.75,(255,255,255),1,cv2.LINE_AA)# Awsm Smooth lines.
        cv2.putText(img,'PRESS c TO CLEAR',(100,630), font, 0.75,(255,255,255),1,cv2.LINE_AA)
        
    else:
        cv2.putText(img,'PRESS h TO TOGGLE  HELP OFF/ON',(45,630), font, 0.7,(255,255,255),1,cv2.LINE_AA)
        
    #cv2.putText(img,'PaintTM',(160,600), font, 1,(255,255,255),2,cv2.LINE_AA)
    
#cv2.waitKey(0)
cv2.destroyAllWindows()


# In[ ]:


import cv2
import numpy as np
import os
# we are going to make a slide show using cv2.addWeighted(img,0.7,img_inv,0.3,0)function and clever use of loops

#we need a namedWindow
cv2.namedWindow('SlideShow')
directory='..\Images'# check if these are correctly put slashes.
fileNames=os.listdir(directory)
i=1
path=0
#get a starting image outside the loop and get images from file 1 by one. When the images end,
# the return value will help us terminate the loop(while(True)<<one )
img1=cv2.imread('G:\Programming\opencv\Images\img2.jpg')
flag=False
i=1;
while(i<len(fileNames) and flag==False):
    
    if fileNames[i].endswith(".jpg") or fileNames[i].endswith(".png") :
        path=os.path.join(directory,fileNames[i])

    else:
        i=i+1
        continue
    img2=cv2.imread(path) # for testing
    #img2=cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    if not len(img1) or not len(img2):
        break
    for j in range(1,50):
        #print(img1.shape, img2.shape)
        img1= cv2.addWeighted(img1,1-j/100.0,img2,j/100.0,0)
        #img1=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
        cv2.imshow('slideShow',img1)
        if cv2.waitKey(40) & 0xFF==ord('a') : # initially there is very little change in image 1 so image stays static, then image 2 takes over and changes image 1. So the transition works very smothly.
            break # this is to speed through the pictures
    cv2.waitKey(50)                    # add some delay show the image before switching to other image
    i=i+1
    
cv2.destroyAllWindows()

