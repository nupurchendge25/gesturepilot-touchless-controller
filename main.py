
import cv2
import mediapipe as mp
import pyautogui
import time

# -------------------- SETTINGS --------------------

pyautogui.FAILSAFE = True

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

IMG_WIDTH = 640
IMG_HEIGHT = 480

# Cursor settings
dead_zone = 3
prev_x, prev_y = screen_width // 2, screen_height // 2

# Cursor control region
x_min, x_max = 0.15, 0.85
y_min, y_max = 0.15, 0.85

# Gesture settings
pinch_threshold = 0.045
drag_hold_time = 0.35

control_enabled = True
dragging = False
pinch_start_time = None

# Scroll settings
previous_scroll_y = None
scroll_threshold = 0.008
scroll_sensitivity = 3000

# Canny edge detection
edge_mode = False

# FPS
previous_frame_time = time.time()
fps = 0

# -------------------- MAIN PROGRAM --------------------

try:
    with mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6
    ) as hands:

        while cap.isOpened():

            success, frame = cap.read()

            if not success:
                break

            # 1. Image acquisition and resizing
            frame = cv2.resize(frame, (IMG_WIDTH, IMG_HEIGHT))

            # Mirror webcam image
            frame = cv2.flip(frame, 1)

            # 2. Convert BGR to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            status = "NO HAND DETECTED"
            pixel_text = "Pixel BGR: N/A"

            # Draw cursor control region
            cv2.rectangle(
                frame,
                (int(x_min * IMG_WIDTH), int(y_min * IMG_HEIGHT)),
                (int(x_max * IMG_WIDTH), int(y_max * IMG_HEIGHT)),
                (255, 255, 0),
                2
            )

            if results.multi_hand_landmarks:

                hand = results.multi_hand_landmarks[0]
                landmarks = hand.landmark

                mp_draw.draw_landmarks(
                    frame,
                    hand,
                    mp_hands.HAND_CONNECTIONS
                )

                thumb = landmarks[4]
                index = landmarks[8]
                middle = landmarks[12]
                ring = landmarks[16]
                pinky = landmarks[20]

                # 3. Pixel-value analysis at index fingertip
                ix = max(
                    0, min(IMG_WIDTH - 1, int(index.x * IMG_WIDTH))
                )
                iy = max(
                    0, min(IMG_HEIGHT - 1, int(index.y * IMG_HEIGHT))
                )

                b, g, r = frame[iy, ix]
                pixel_text = f"Pixel BGR: {b}, {g}, {r}"

                cv2.circle(
                    frame, (ix, iy), 7, (0, 255, 255), -1
                )

                if control_enabled:

                    # Map fingertip position to screen coordinates
                    target_x = int(
                        (index.x - x_min) / (x_max - x_min)
                        * screen_width
                    )
                    target_y = int(
                        (index.y - y_min) / (y_max - y_min)
                        * screen_height
                    )

                    target_x = max(
                        0, min(screen_width - 1, target_x)
                    )
                    target_y = max(
                        0, min(screen_height - 1, target_y)
                    )

                    # 4. Adaptive cursor smoothing
                    dx = target_x - prev_x
                    dy = target_y - prev_y

                    # Ignore tiny movements to reduce jitter
                    if abs(dx) < dead_zone:
                        dx = 0

                    if abs(dy) < dead_zone:
                        dy = 0

                    distance = (dx ** 2 + dy ** 2) ** 0.5

                    # Faster response for larger movements
                    if distance > 100:
                        factor = 0.65
                    elif distance > 20:
                        factor = 0.40
                    else:
                        factor = 0.75

                    curr_x = prev_x + dx * factor
                    curr_y = prev_y + dy * factor

                    # 5. Detect scrolling gesture:
                    # Index and middle fingers up;
                    # ring and little fingers down.
                    scroll_mode = (
                        index.y < landmarks[6].y
                        and middle.y < landmarks[10].y
                        and ring.y > landmarks[14].y
                        and pinky.y > landmarks[18].y
                    )

                    if scroll_mode:

                        status = "SCROLL MODE"

                        if previous_scroll_y is not None:

                            movement = index.y - previous_scroll_y

                            if abs(movement) > scroll_threshold:

                                # Preserve calculated scroll amount
                                scroll_amount = int(
                                    -movement * scroll_sensitivity
                                )

                                # Ensure small movements still scroll
                                if scroll_amount == 0:
                                    scroll_amount = (
                                        -1 if movement > 0 else 1
                                    )

                                pyautogui.scroll(scroll_amount)

                        previous_scroll_y = index.y

                    else:

                        previous_scroll_y = None

                        # Move cursor
                        pyautogui.moveTo(
                            int(curr_x), int(curr_y)
                        )

                        prev_x, prev_y = curr_x, curr_y

                        # 6. Detect thumb-index pinch
                        distance_pinch = (
                            (thumb.x - index.x) ** 2
                            + (thumb.y - index.y) ** 2
                        ) ** 0.5

                        pinch_active = (
                            distance_pinch < pinch_threshold
                        )

                        if pinch_active:

                            if pinch_start_time is None:
                                pinch_start_time = time.time()

                            held_time = (
                                time.time() - pinch_start_time
                            )

                            # Hold pinch to start dragging
                            if (
                                held_time >= drag_hold_time
                                and not dragging
                            ):
                                pyautogui.mouseDown()
                                dragging = True

                            if dragging:
                                status = "DRAGGING"
                            else:
                                status = "PINCH / CLICK"

                        else:

                            # Release drag or perform click
                            if pinch_start_time is not None:

                                if dragging:
                                    pyautogui.mouseUp()
                                    dragging = False
                                else:
                                    pyautogui.click()

                                pinch_start_time = None

                            status = "CURSOR CONTROL: ON"

                else:

                    status = "PAUSED"

                    if dragging:
                        pyautogui.mouseUp()
                        dragging = False

                    pinch_start_time = None
                    previous_scroll_y = None

            else:

                # Release mouse if hand disappears
                if dragging:
                    pyautogui.mouseUp()
                    dragging = False

                pinch_start_time = None
                previous_scroll_y = None

            # ---------------- IMAGE PROCESSING ----------------

            # 7. Convert image to grayscale
            gray_frame = cv2.cvtColor(
                frame, cv2.COLOR_BGR2GRAY
            )

            # 8. Optional Canny edge detection
            if edge_mode:
                edges = cv2.Canny(gray_frame, 100, 200)
                cv2.imshow("Canny Edge Detection", edges)
            else:
                try:
                    cv2.destroyWindow("Canny Edge Detection")
                except cv2.error:
                    pass

            # ---------------- DISPLAY INFORMATION ----------------

            # Calculate FPS
            current_time = time.time()
            elapsed = current_time - previous_frame_time

            if elapsed > 0:
                instant_fps = 1 / elapsed
                fps = 0.9 * fps + 0.1 * instant_fps

            previous_frame_time = current_time

            # Status color
            if not control_enabled:
                status_color = (0, 165, 255)
            elif dragging:
                status_color = (0, 0, 255)
            else:
                status_color = (0, 255, 0)

            cv2.putText(
                frame, status, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65, status_color, 2
            )

            cv2.putText(
                frame, f"FPS: {fps:.1f}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55, (255, 255, 255), 2
            )

            cv2.putText(
                frame, pixel_text, (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 1
            )

            cv2.putText(
                frame,
                "P: Pause | C: Canny | Q: Quit",
                (10, IMG_HEIGHT - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 1
            )

            cv2.imshow("GesturePilot", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

            elif key == ord("p"):

                control_enabled = not control_enabled

                if not control_enabled:

                    if dragging:
                        pyautogui.mouseUp()
                        dragging = False

                    pinch_start_time = None
                    previous_scroll_y = None

            elif key == ord("c"):
                edge_mode = not edge_mode

finally:

    # Release mouse button safely on exit
    if dragging:
        try:
            pyautogui.mouseUp()
        except Exception:
            pass

    cap.release()
    cv2.destroyAllWindows()
