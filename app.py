import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="PPE Detection",
    page_icon="🦺",
    layout="wide"
)

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🦺 PPE Detection using YOLOv8")

st.write(
    "Upload a construction-site image to detect "
    "Personal Protective Equipment (PPE)."
)

# --------------------------------------------------
# Load YOLO Model
# --------------------------------------------------

model = YOLO("yolov8n.pt")

# --------------------------------------------------
# Upload Image
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload a construction worker image",
    type=["jpg", "jpeg", "png"]
)

# --------------------------------------------------
# Detection
# --------------------------------------------------

if uploaded_file is not None:

    # Read uploaded image
    image = Image.open(uploaded_file)

    # Display original image
    st.subheader("📷 Original Image")
    st.image(image, use_container_width=True)

    # Convert PIL image to NumPy array
    img_array = np.array(image)

    # Run YOLO detection
    results = model(img_array)

    # Draw detection boxes
    result_image = results[0].plot()

    # Display detection result
    st.subheader("🔍 PPE Detection Result")
    st.image(result_image, use_container_width=True)

    # --------------------------------------------------
    # Detection Details
    # --------------------------------------------------

    st.subheader("📊 Detected PPE")

    boxes = results[0].boxes

    if boxes is not None and len(boxes) > 0:

        for box in boxes:

            # Class ID
            class_id = int(box.cls[0])

            # Confidence
            confidence = float(box.conf[0])

            # Class name
            class_name = model.names[class_id]

            st.write(
                f"**{class_name}** → Confidence: {confidence:.2%}"
            )

    else:
        st.warning("⚠️ No PPE detected.")