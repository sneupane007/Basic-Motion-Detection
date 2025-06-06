# Frame differencing 
import cv2 
from src.utils.event_logger import log_motion_event

def start_motion_detection():
    cap = cv2.VideoCapture(0)
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    #Background Subtraction
    backSub = cv2.createBackgroundSubtractorMOG2()

    try:
        while True:
            fgMask = backSub.apply(frame1,frame2)
            diff = cv2.absdiff(frame1, frame2)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5,5), 0)
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh, None, iterations=3)
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            #Log motion 
            if contours:
                log_motion_event()

            #rectangles 
            for contour in contours:
                if cv2.contourArea(contour) < 1000:
                    continue
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame1, (x,y), (x+w, y+h), (0,255,0), 2)
            
            cv2.imshow('Motion Detection', frame1)
            frame1 = frame2
            ret, frame2 = cap.read()
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    start_motion_detection() 