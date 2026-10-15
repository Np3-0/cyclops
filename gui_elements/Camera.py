from PySide6.QtCore import Signal, QObject 
from pylibdmtx.pylibdmtx import decode
import cv2
import time
import requests

class Camera(QObject):
    frame_captured = Signal(object)
    dye_found = Signal(dict)
    last_code = ""
    
    def __init__(self, cam, parent=None):
        super().__init__(parent)
        self.cam = cam
        self.running = False
    
    def run(self):
        self.running = True
        cap = cv2.VideoCapture(self.cam, cv2.CAP_DSHOW)
        while self.running:
            ret, frame = cap.read()
            if not ret: break
            
            # turn frame gray specifically for data matrix
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            result = decode(gray, max_count=1, timeout=100)
            if result:
                code = result[0]
                # draws rectangle where the code is
                rect = code.rect
                y = frame.shape[0] - rect.top - rect.height
                cv2.rectangle(frame, (rect.left, y), (rect.left + rect.width, y + rect.height), (0, 255, 0), 3)
                
                text = code.data.decode("utf-8")

                # prevents api from calling same code twice in a row
                if (text != self.last_code):
                    self.last_code = text
                    try:
                        res = requests.get(f"https://inventory-api-892294444215.us-east1.run.app/dyes/{text}")
                        res.raise_for_status()
                        self.dye_found.emit(res.json())
                    except requests.RequestException as e:
                        print(f"API Error: {e}")
                    
                
                time.sleep(0.5)
            
            self.frame_captured.emit(frame)
            time.sleep(0.033)
        
        cap.release()
    
    def stop(self):
        self.running = False