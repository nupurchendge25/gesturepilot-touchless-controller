
import cv2
import mediapipe as mp
import pyautogui

pyautogui.FAILSAFE = True

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

prev_x, prev_y = 0, 0
smoothening = 2

control_enabled = True
dragging = False
pinch_was_active = False

try:
    with mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as hands:

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[0]

                mp_draw.draw_landmarks(
                    frame, hand, mp_hands.HAND_CONNECTIONS
                )

                # Index fingertip controls the cursor
                index = hand.landmark[8]
                target_x = int(index.x * screen_width)
                target_y = int(index.y * screen_height)

                curr_x = prev_x + (target_x - prev_x) / smoothening
                curr_y = prev_y + (target_y - prev_y) / smoothening

                if control_enabled:
                    pyautogui.moveTo(int(curr_x), int(curr_y))

                prev_x, prev_y = curr_x, curr_y

                # Detect pinch between thumb and index finger
                thumb = hand.landmark[4]
                distance = (
                    (thumb.x - index.x) ** 2
                    + (thumb.y - index.y) ** 2
                ) ** 0.5

                pinch_active = distance < 0.07

                # Pinch and hold to drag; release fingers to drop
                if control_enabled:
                    if pinch_active and not dragging:
                        pyautogui.mouseDown()
                        dragging = True

                    elif not pinch_active and dragging:
                        pyautogui.mouseUp()
                        dragging = False

                elif dragging:
                    pyautogui.mouseUp()
                    dragging = False

                pinch_was_active = pinch_active

                if dragging:
                    status = "DRAGGING"
                elif not control_enabled:
                    status = "PAUSED"
                elif pinch_active:
                    status = "PINCH DETECTED"
                else:
                    status = "CURSOR CONTROL: ON"

                cv2.putText(
                    frame, status, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 0, 255) if dragging or pinch_active
                    else (0, 255, 0), 2
                )

            else:
                # Release a drag if the hand disappears
                if dragging:
                    pyautogui.mouseUp()
                    dragging = False

                pinch_was_active = False

            cv2.imshow("GesturePilot", frame)
            cv2.setWindowProperty(
            "GesturePilot", cv2.WND_PROP_TOPMOST, 1
            )

            key = cv2.waitKey(10) & 0xFF

            if key == ord("q"):
                break
            elif key == ord("p"):
                control_enabled = not control_enabled

finally:
    # Prevent the mouse button remaining held after exit
    if dragging:
        pyautogui.mouseUp()

    cap.release()
    cv2.destroyAllWindows()
