import cv2
import time
from yolo_model import detect_objects, draw_detections, count_by_class
from ppe_model  import detect_ppe, draw_boxes, check_compliance


def run_on_image(image_path):
    print("Running on image:", image_path)

    image = cv2.imread(image_path)

    # general detection
    yolo_dets = detect_objects(image_path)
    image     = draw_detections(image, yolo_dets)

    # PPE detection
    ppe_dets = detect_ppe(image_path)
    image    = draw_boxes(image, ppe_dets)

    check_compliance(ppe_dets)

    print("Object counts:", count_by_class(yolo_dets))

    cv2.imwrite("vision_output.jpg", image)
    print("Saved to vision_output.jpg")

    cv2.imshow("Result", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def run_webcam():
    print("Starting webcam... Press 'q' to quit.")
    cap = cv2.VideoCapture(0)

    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # calculate FPS
        now      = time.time()
        fps      = 1 / (now - prev_time + 0.001)
        prev_time = now

        # run detections on current frame
        yolo_dets = detect_objects(frame, conf=0.4)
        ppe_dets  = detect_ppe(frame, conf=0.4)

        frame = draw_detections(frame, yolo_dets)
        frame = draw_boxes(frame, ppe_dets)

        # show FPS on screen
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # show person count
        counts = count_by_class(yolo_dets)
        cv2.putText(frame, f"Persons: {counts.get('person', 0)}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        # show violation warning
        violations = [d["class"] for d in ppe_dets if d["violation"]]
        if violations:
            cv2.putText(frame, "VIOLATION DETECTED!", (10, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow("Safety Vision Monitor", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


# main
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        run_on_image(sys.argv[1])
    else:
        run_webcam()
