import cv2
import time
from pynput.mouse import Listener 



def show_xy(event,x,y,flags,userdata):
    if (event == 1) :
        cv2.circle(userdata, (x,y), 3, (0,0,255), 5, 16)
        print("get origin points: (x, y) = ({}, {})".format(x, y)) 
        print(event,x,y,flags)
    
cap = cv2.VideoCapture('test.mov')            # 讀取某個影片


    


print("---------------------------")



tracker_list = []
for i in range(1):
    tracker = cv2.TrackerCSRT_create()        # 創建一組追蹤器
    tracker_list.append(tracker)
colors = [(0,0,255)]  # 設定外框顏色
tracking = False                              # 設定 False 表示尚未開始追蹤

a = 0                                         # 刪減影片影格使用

if not cap.isOpened():                        #防止crash
    print("Cannot open camera")
    
    exit()

counter = 1
while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Cannot receive frame, stop tracking")
        break

    keyName = cv2.waitKey(1)
  
    if a%1 == 0:
        if keyName == ord('q'):        #按下q停止程式
            break
        if tracking == False:
            # 如果尚未開始追蹤，就開始標記追蹤物件的外框
            for i in tracker_list:
     
                area = cv2.selectROI('oxxostudio', frame, showCrosshair=False, fromCenter=False)
                
                cv2.setMouseCallback('oxxostudio', show_xy)
                
                i.init(frame, area)    # 初始化追蹤器
            tracking = True            # 設定可以開始追蹤
            start = time.time()
        if tracking:
            
            for i in range(len(tracker_list)):
                success, point = tracker_list[i].update(frame)   # 追蹤成功後，不斷回傳左上和右下的座標
                
                if success:
                    p1 = [int(point[0]), int(point[1])]
                    p2 = [int(point[0] + point[2]), int(point[1] + point[3])]
                    cv2.rectangle(frame, p1, p2, colors[i], 1)   # 根據座標，繪製四邊形，框住要追蹤的物件 cv2.rectangle(image, start_point, end_point, color, thickness)
                    print("(",p1,")","and","(",p2,")",counter)
                    counter = counter + 1
        cv2.imshow('oxxostudio', frame)
    a = a + 1
    

cap.release()
cv2.destroyAllWindows()


