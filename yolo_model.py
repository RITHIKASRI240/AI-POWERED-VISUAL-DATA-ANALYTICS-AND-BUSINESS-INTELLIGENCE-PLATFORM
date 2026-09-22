import cv2
from ultralytics import YOLO

# yolov8n.pt will auto-download if not present
model = YOLO("yolov8n.pt")


def detect_objects(image_path, conf=0.35):
    results = model.predict(image_path, conf=conf, verbose=False)

    detections = []
    for r in results:
        for box in r.boxes:
            cls_id   = int(box.cls[0])
            cls_name = model.names[cls_id]
            conf_val = round(float(box.conf[0]), 2)
            x1, y1, x2, y2 = [int(v) for v in box.xyxy[0]]

            detections.append({
                "class": cls_name,
                "conf" : conf_val,
                "box"  : [x1, y1, x2, y2]
            })

    return detections


def draw_detections(image, detections):
    for d in detections:
        x1, y1, x2, y2 = d["box"]
        label = f"{d['class']} {d['conf']}"
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 150, 0), 2)
        cv2.putText(image, label, (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 150, 0), 1)
    return image


def count_by_class(detections):
    counts = {}
    for d in detections:
        name = d["class"]
        counts[name] = counts.get(name, 0) + 1
    return counts


# test
if __name__ == "__main__":
    import sys

    img_path = sys.argv[1] if len(sys.argv) > 1 else "test_image.jpg"

    detections = detect_objects(img_path)
    counts     = count_by_class(detections)

    print(f"Detected {len(detections)} object(s):")
    for cls, n in counts.items():
        print(f"  {cls}: {n}")

    image  = cv2.imread(img_path)
    output = draw_detections(image, detections)
    cv2.imwrite("yolo_output.jpg", output)
    print("Saved to yolo_output.jpg")
