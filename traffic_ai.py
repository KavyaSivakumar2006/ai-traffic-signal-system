from ultralytics import YOLO
import cv2
import time

print("Starting AI Smart Traffic Signal System...")

# Load YOLOv8 nano model (pre-trained on COCO)
model = YOLO("yolov8n.pt")

# Start webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Webcam not detected!")
    exit()

# Initial signal values
signal_color = "RED"
signal_time = None
last_update_time = time.time()
traffic_cycle_started = False

# Calibrated timing model (seconds)
BASE_GREEN_SEC = 6
SEC_PER_UNIT = 1.8
MIN_GREEN_SEC = 8
MAX_GREEN_SEC = 45
YELLOW_SEC = 4
RED_SEC = 10
SMOOTHING_ALPHA = 0.3

# Passenger car unit style weights (heavier vehicles need more discharge time)
VEHICLE_WEIGHTS = {
    "motorbike": 0.5,
    "car": 1.0,
    "bus": 2.5,
    "truck": 2.5,
}

smoothed_units = 0.0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    frame = cv2.resize(frame, (640, 480))

    # Run detection
    results = model(frame, verbose=False)

    vehicle_count = 0
    vehicle_units = 0.0

    # Count vehicles
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            label = model.names[class_id]

            if label in VEHICLE_WEIGHTS:
                vehicle_count += 1
                vehicle_units += VEHICLE_WEIGHTS[label]

                # Draw bounding box
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # -------------------------
    # 🚦 Dynamic Signal Logic
    # -------------------------

    smoothed_units = (SMOOTHING_ALPHA * vehicle_units) + ((1 - SMOOTHING_ALPHA) * smoothed_units)
    effective_units = max(vehicle_units, smoothed_units)
    green_duration = int(round(BASE_GREEN_SEC + (SEC_PER_UNIT * effective_units)))
    green_duration = max(MIN_GREEN_SEC, min(MAX_GREEN_SEC, green_duration))

    current_time = time.time()

    # Pause and reset signal cycle when no vehicles are detected.
    if vehicle_count == 0:
        traffic_cycle_started = False
        signal_color = "RED"
        signal_time = None
        remaining_time = 0
    else:
        # Start timer only after at least one vehicle is detected.
        if not traffic_cycle_started:
            traffic_cycle_started = True
            signal_color = "GREEN"
            signal_time = green_duration
            last_update_time = current_time

        # Update signal state
        if signal_color == "RED":
            if current_time - last_update_time >= signal_time:
                signal_color = "GREEN"
                signal_time = green_duration
                last_update_time = current_time

        elif signal_color == "GREEN":
            # Allow only upward adjustment while green is active when demand increases.
            signal_time = max(signal_time, green_duration)
            if current_time - last_update_time >= signal_time:
                signal_color = "YELLOW"
                signal_time = YELLOW_SEC
                last_update_time = current_time

        elif signal_color == "YELLOW":
            if current_time - last_update_time >= signal_time:
                signal_color = "RED"
                signal_time = RED_SEC
                last_update_time = current_time

        # Countdown
        remaining_time = max(0, int(signal_time - (current_time - last_update_time)))

    # -------------------------
    # 📊 Display Dashboard
    # -------------------------

    cv2.putText(frame, f"Vehicle Count: {vehicle_count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.putText(frame, f"Demand Units: {effective_units:.1f}", (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.putText(frame, f"Signal: {signal_color}", (20, 105),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    if traffic_cycle_started:
        time_text = f"Time Left: {remaining_time} sec"
    else:
        time_text = "Time Left: --"

    cv2.putText(frame, time_text, (20, 140),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.putText(frame, f"Planned Green: {green_duration} sec", (20, 175),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    if not traffic_cycle_started:
        cv2.putText(frame, "Waiting for vehicle detection...", (20, 210),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)

    # Draw signal indicator circle
    if signal_color == "RED":
        color = (0, 0, 255)
    elif signal_color == "YELLOW":
        color = (0, 255, 255)
    else:
        color = (0, 255, 0)

    cv2.circle(frame, (550, 70), 20, color, -1)

    cv2.imshow("AI Smart Traffic Signal System", frame)

    if cv2.waitKey(1) == 27:  # Press ESC to exit
        break

cap.release()
cv2.destroyAllWindows()