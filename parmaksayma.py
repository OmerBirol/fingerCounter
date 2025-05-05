import cv2
import mediapipe as mp

cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

mphand=mp.solutions.hands
hands=mphand.Hands()
mpDraw=mp.solutions.drawing_utils#elind üstündeki iskelet kısmı oluşturur



tipId=[4,8,12,16,20]
while True:
    success,img=cap.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)#koordinatları yazdırır
    #print(results)
    
    lmList=[]
    
    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img,handlms,mphand.HAND_CONNECTIONS)
            
            for id , lm in enumerate(handlms.landmark):
                h,w,_=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy])
                
                #işaret uç 
                if id==8:
                    cv2.circle(img,(cx,cy),9,(255,0,0),cv2.FILLED)
                
                if id==6:
                    cv2.circle(img,(cx,cy),9,(0,255,0),cv2.FILLED)
    
    
    if len(lmList)!=0:
        finger=[]
        #sağ sol el tespit
        
        if lmList[tipId[0]][1]<lmList[tipId[1]][1]:
            cv2.putText(img,"Sol",(50,300),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),8)
        else:
            if lmList[tipId[0]][1] > lmList[tipId[0]-1][1]:
                finger.append(1)
            else:
                finger.append(0)
            cv2.putText(img,"Sag",(50,300),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),8)
        
        
        #baş parmak
        if lmList[tipId[0]][1] < lmList[tipId[0]-1][1]:
            finger.append(1)
        else:
            finger.append(0)
        
        #4 parmak için
        for id in range(1,5):
            #eklemlerdeki iki alt eklem kapandığında alta geldiği için 2 çıkartıyoruz ve ikisinin koordinatlarının aynı olöması sebebi elimizi dik tutarak çalışmamız
            if lmList[tipId[id]][2] < lmList[tipId[id]-2][2]:
                finger.append(1)
                
            else:
                finger.append(0)
                
        totalF=finger.count(1)
        cv2.putText(img,str(totalF),(30,125),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),8)
        
    
                
            
            
    
    
    
    
    
    
    
    
   # print(lmList)
    
    
    
    
    cv2.imshow("Video",img)
    cv2.waitKey(1)
