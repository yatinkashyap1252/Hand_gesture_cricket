import cv2
from cvzone.HandTrackingModule import HandDetector
import random
import time

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=1)

user_score = 0
computer_choice = None
new_round = True
user_runs = 0
score_updated = False
out_time = None

def map_user_runs(fingers):
    if fingers == [1, 0, 0, 0, 0]: 
        return 10
    elif fingers == [0, 1, 0, 0, 0]:  
        return 1
    elif fingers == [0, 1, 1, 0, 0]:  
        return 2
    elif fingers == [0, 1, 1, 1, 0]:  
        return 3
    elif fingers == [0, 1, 1, 1, 1]:  
        return 4
    elif fingers == [1, 1, 1, 1, 1]:  
        return 5
    elif fingers == [1, 0, 0, 0, 0]:  
        return 6
    elif fingers == [1, 1, 0, 0, 0]:  
        return 7
    elif fingers == [1, 1, 1, 0, 0]:  
        return 8
    elif fingers == [1, 0, 1, 1, 1]:  
        return 9
    else:
        return 0  

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    if hands and (out_time is None or time.time() - out_time >= 2):
        hand1 = hands[0]
        fingers = detector.fingersUp(hand1)
        user_runs = map_user_runs(fingers)

        if new_round:
            computer_choice = random.choice(range(1, 11))
            score_updated = False
            new_round = False

        if user_runs == computer_choice and not score_updated:
            cv2.putText(img, "Out!", (550, 350), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255), 8)
            user_score = 0
            score_updated = True
            out_time = time.time()
        elif not score_updated:
            user_score += user_runs
            score_updated = True

    if out_time and time.time() - out_time < 2:
        cv2.putText(img, "Out!", (550, 350), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255), 8)

    if not new_round:
        cv2.putText(img, f"Computer Choice: {computer_choice}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(img, f"User Score: {user_score}", (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(img, f"User Runs: {user_runs}", (30, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.putText(img, "Press 'N' for New Round or 'Q' to Quit", (30, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    if cv2.waitKey(1) & 0xFF == ord('n'):
        new_round = True
        user_runs = 0

    cv2.imshow("Cricket Hand Game", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()