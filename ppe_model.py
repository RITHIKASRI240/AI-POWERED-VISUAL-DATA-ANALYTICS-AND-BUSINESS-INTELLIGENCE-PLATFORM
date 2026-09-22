import cv2
from ultralytics import YOLO

# load the PPE model
model = YOLO("best.pt")

# class names from your training
# update this list to match your best.pt labels
CLASS_NAMES = {
    0: "hardhat",
    1: "safety-vest",
    2: "gloves",
    3: "goggles",
    4: "mask",
    5: "no-hardhat",
    6: "no-safety-vest",
}

VIOLATION_CLASSES = ["no-hardhat", "no-safety-vest"]


def detect_ppe(image_path, conf=0.4):
    results = model.predict(image_path, conf=conf, verbose=False)

    detections = []
    for r in results:
        for box in r.boxes:
            cls_id   = int(box.cls[0])
            cls_name = CLASS_NAMES.get(cls_id, "unknown")
            conf_val = round(float(box.conf[0]), 2)
            x1, y1, x2, y2 = [int(v) for v in box.xyxy[0]]

            detections.append({
                "class"    : cls_name,
                "conf"     : conf_val,
                "box"      : [x1, y1, x2, y2],
                "violation": cls_name in VIOLATION_CLASSES
            })

    return detections


def draw_boxes(image, detections):
    for d in detections:
        x1, y1, x2, y2 = d["box"]
        color = (0, 0, 255) if d["violation"] else (0, 255, 0)
        label = f"{d['class']} {d['conf']}"

        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, label, (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    return image


def check_compliance(detections):
    violations = [d["class"] for d in detections if d["violation"]]
    if violations:
        print("VIOLATIONS FOUND:", violations)
        return False
    else:
        print("All PPE compliant!")
        return True


# test
if __name__ == "__main__":
    import sys

    img_path = sys.argv[1] if len(sys.argv) > 1 else "test_image.jpg"

    image      = cv2.imread(img_path)
    detections = detect_ppe(img_path)

    print(f"\nDetected {len(detections)} objects:")
    for d in detections:
        print(f"  {d['class']} ({d['conf']}) - violation: {d['violation']}")

    check_compliance(detections)

    output = draw_boxes(image, detections)
    cv2.imwrite("ppe_output.jpg", output)
    print("\nSaved to ppe_output.jpg")
