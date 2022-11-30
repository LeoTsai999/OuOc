import cv2
import time
from pynput.mouse import Listener 

click = False
centerL = 0
centerT = 0
def clicked(x, y, button, is_press):
    if is_press:
        global click,centerL,centerT
        centerL = x
        centerT = y
        click = True

listener = Listener(on_click=clicked)

time.sleep(1)
print("detection start")
listener.start()
while True:
    if click:
        listener.stop()
        print("successfully,","O(",[centerL , centerT ],")")
        break



cap = cv2.VideoCapture('test.mov')            # 讀取某個影片

tracker_list = []
for i in range(1):
    tracker = cv2.TrackerCSRT_create()        # 創建c一組追蹤器
    tracker_list.append(tracker)
colors = [(0,0,255)]  # 設定外框顏色
tracking = False                              # 設定 False 表示尚未開始追蹤

print("line13")

a = 0                                         # 刪減影片影格使用


if not cap.isOpened():                        #防止crash
    print("Cannot open camera")
    
    exit()
print("line21")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Cannot receive frame")
        break
    print("line27")
    keyName = cv2.waitKey(1)
  
    if a%1 == 0:
        if keyName == ord('q'):
            break
        if tracking == False:
            # 如果尚未開始追蹤，就開始標記追蹤物件的外框
            for i in tracker_list:
                print("line36")
                area = cv2.selectROI('oxxostudio', frame, showCrosshair=False, fromCenter=False)
                print("line38")
                i.init(frame, area)    # 初始化追蹤器
                print("line40")
            tracking = True            # 設定可以開始追蹤
            start = time.time()
        if tracking:
            counter = 1
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
print("line51")
cap.release()
cv2.destroyAllWindows()



#Imshow
#偵測滑鼠位置
#
