import cv2
from pylibdmtx.pylibdmtx import decode
import webbrowser
import constants

def scan_matrix():
    found = False
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open camera.")
        return
    
    while True:
        ret, frame = cap.read()
    
        if not ret:
            print("Image not found.")
            break
    
        # turn frame gray to make processing easier
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Press Q to quit.", gray)

        code = decode(gray)
        if code:
            c = code[0]
            text = c.data.decode("utf-8")
            webbrowser.open(constants.API_URL + f"/dyes/{text}")
            found = True
            
            
            
        else:
            print("Not found.")
        
        if (cv2.waitKey(1) & 0xFF == ord("q") or found):
            break
        
    cv2.destroyAllWindows()
    cap.release()
    
if __name__ == "__main__":
    scan_matrix()