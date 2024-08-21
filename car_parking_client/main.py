import cv2
import time
import requests
# from .test import convert2IntArr

cap = cv2.VideoCapture('CarPark.mp4')
delay = 120

parking_slots2 = [(402, 239), (753, 377), (55, 100), (56, 146), (51, 241), (53, 290), (51, 192), (405, 189), (402, 138), (405, 90), (514, 92), (511, 139), (514, 187), (512, 236), (163, 99), (164, 147), (158, 194), (159, 243), (161, 290), (55, 337), (162, 339), (160, 388), (162, 429), (52, 431), (53, 479), (163, 479), (168, 525), (165, 576), (165, 620), (56, 623), (51, 573), (52, 527), (402, 289), (402, 338), (404, 382), (405, 427), (405, 526), (403, 569), (406, 619), (512, 524), (512, 568), (513, 620), (511, 426), (511, 380), (513, 329), (511, 284), (751, 88), (751, 136), (750, 188), (753, 232), (753, 276), (751, 327), (757, 427), (753, 472), (757, 518), (760, 573), (760, 616), (901, 620), (901, 576), (892, 141), (892, 190), (893, 235), (894, 284), (897, 330), (898, 375), (901, 424), (903, 474), (899, 522), (46, 385)]

parking_slots = [(55, 100), (163, 99), (56, 146), (164, 147), (51, 192), (158, 194), (51, 241),  (159, 243), (53, 290), (161, 290), (55, 337),  (162, 339), (46, 385), (160, 388), (52, 431), (162, 429), (53, 479) , (163, 479), (52, 527), (168, 525),(51, 573),(165, 576), (56, 623), (165, 620), (405, 90), (514, 92), (402, 138), (511, 139), (405, 189), (514, 187), (402, 239), (512, 236),  (402, 289), (511, 284), (402, 338), (513, 329), (404, 382), (511, 380), (405, 427), (511, 426), (405, 526),  (512, 524),  (403, 569), (512, 568), (406, 619), (513, 620), (751, 88), (892, 141), (751, 136), (892, 190),(750, 188),(893, 235), (753, 232), (894, 284), (753, 276),(897, 330), (751, 327), (898, 375), (753, 377), (901, 424),  (757, 427), (903, 474), (753, 472), (899, 522), (757, 518), (901, 576), (760, 573), (901, 620),(760, 616)]

rect_width, rect_height = 100, 33
color = (0,0,255)
thick = 1
threshold = 10
last_call_time = time.time()
prevFreeslots=0


def convert_grayscale(frame):
    # Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply threshold to create a binary image
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # okay, now create a black canvas with the same dimensions as input image
    contour_image = frame.copy()
    contour_image[:] = 0  # Fill with black

    # Draw contours on black canvas in white
    cv2.drawContours(contour_image, contours, -1, (255, 255, 255), thickness=1)
    return contour_image


def mark_slots(frame, grayscale_frame):
    freeSlotsArr = []
    global last_call_time
    global prevFreeslots
    current_time = time.time()
    elapsed_time = current_time - last_call_time

    freeslots=0
    slotNo = 0

    freeSlotsArr.clear()

    for x, y in parking_slots:
        x1=x+10
        x2=x+rect_width-11
        y1=y+4
        y2=y+rect_height
        start_point, stop_point = (x1,y1), (x2, y2)

        crop=grayscale_frame[y1:y2, x1:x2]
        gray_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

        # Get count of non-zero pixels
        count=cv2.countNonZero(gray_crop)

        #Assign color, thickness based on threshold
        color, thick = [(0,255,0), 3] if count<threshold else [(0,0,255), 3]

        slotNo = slotNo + 1
        if count<threshold:
            freeslots = freeslots+1
            freeSlotsArr.append(slotNo)
        cv2.rectangle(frame, start_point, stop_point, color, thick)
        cv2.putText(frame, "Slots:" + str(slotNo), (x+12, y+25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 255, 255), 1)

        # Uncomment to display non-zero pixel count in each parking slot rectangle
        # text_x = x1+5
        # text_y = y1 + 10  # Adjust the Y-coordinate to position the text above the rectangle
        # cv2.putText(frame, str(count), (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 255, 255), 1)

    #Update the Free Slots display counter - less frequently
    # print(freeSlotsArr, len(freeSlotsArr))
    current_time = time.time()
    if current_time - last_call_time >= 0.1:
        cv2.putText(frame, "Free Slots:" + str(freeslots), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 255, 255), 2)
        last_call_time = current_time
        prevFreeslots = freeslots
    else:
         cv2.putText(frame, "Free Slots:" + str(prevFreeslots), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 255, 255), 2)
    return (frame, freeSlotsArr)
    
def test_slots(frame):  
    # print(len(parking_slots))
    slotNo = 0
    for x, y in parking_slots:
        x1=x+10
        x2=x+rect_width-11
        y1=y+4
        y2=y+rect_height
        start_point, stop_point = (x1,y1), (x2, y2)

        #Assign color, thickness based on threshold
        color, thick = [(0,255,0), 5] 

        slotNo = slotNo + 1

        cv2.rectangle(frame, start_point, stop_point, color, thick)
        cv2.putText(frame, "Slots:" + str(slotNo), (x+10, y+25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 255, 255), 2)
    return frame

# print(len(parking_slots))
prevFreeSlots = []
freeSlots = []

while True:
    ret, frame = cap.read()
    # tempo = float(1/delay)
    # time.sleep(tempo) 
    if cv2.waitKey(1) != -1 or not ret:
        break

    grayscale_frame = convert_grayscale(frame)
    out_image, freeSlots = mark_slots(frame, grayscale_frame)
    # out_image = test_slots(frame)
    # cv2.imshow('Origin video', frame)
    cv2.imshow('Parking Spot Detector', out_image)

    freeSlots.sort()
    prevFreeSlots.sort()
    if freeSlots!= prevFreeSlots:
        post_data = {
            'parkingName' : 'parking1',
            'freeSlots' : str(freeSlots),
        }
        prevFreeSlots = freeSlots.copy()
        print(post_data)
        post_url = 'http://127.0.0.1:8000/parking/add/'
        post_response = requests.post(url=post_url, json=post_data)
        print(post_response.text)
    time.sleep(0.1)
# print(len(parking_slots))
cap.release()
cv2.destroyAllWindows()    
