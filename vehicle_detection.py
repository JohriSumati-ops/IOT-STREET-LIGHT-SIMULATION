import cv2
import requests
from collections import defaultdict
import numpy as np

THINGSPEAK_API_KEY = "YOUR_API_KEY"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

def vehicle_detection_and_count():
    cap = cv2.VideoCapture(0)
    vehicle_count = 0
    
    background_subtractor = cv2.createBackgroundSubtractorMOG2()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.resize(frame, (640, 480))
        mask = background_subtractor.apply(frame)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if 500 < area < 5000:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w) / h if h != 0 else 0
                
                if 0.3 < aspect_ratio < 3:
                    vehicle_count += 1
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        cv2.putText(frame, f"Vehicles: {vehicle_count}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Vehicle Detection", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return vehicle_count


def send_to_thingspeak(vehicle_count, lights_status):
    try:
        payload = {
            "api_key": THINGSPEAK_API_KEY,
            "field1": vehicle_count,
            "field2": 1 if lights_status else 0
        }
        
        response = requests.post(THINGSPEAK_URL, data=payload, timeout=5)
        
        if response.status_code == 200:
            print(f"Data sent: Vehicles={vehicle_count}, Lights={'ON' if lights_status else 'OFF'}")
            return True
        else:
            print(f"Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"Connection error: {e}")
        return False


if __name__ == "__main__":
    count = vehicle_detection_and_count()
    send_to_thingspeak(count, count > 0)
