import streamlit as st
import cv2
import subprocess
from pathlib import Path

# ======================
# CONFIGURATION
# ======================
NEW_WIDTH = 640
NEW_HEIGHT = 480

# File paths
THERMAL_IMG_PATH = Path("tes_thermal.jpg")
RGB_IMG_PATH = Path("tes_rgb.jpg")

THERMAL_WEIGHTS = Path("/birdcounter_classifier-seg/seg/w_s/best_thermal_80E.pt")
RGB_WEIGHTS = Path("/bird-counter_classifierseg/seg/w_s/RGB_Segmentation_80E/weights/best_rgb_80E.pt")
PREDICT_SCRIPT = Path("/bird-counter_classifierseg/seg/segment/predict.py")


# ======================
# HELPER FUNCTIONS
# ======================
def set_title():
    """Display dashboard title."""
    st.markdown(
        """
        <style>
        .center {
            display: flex;
            justify-content: center;
            text-align: center;
        }
        </style>
        <div class='center'><h1>🐦 Bird Counter & Detector Dashboard</h1></div>
        """,
        unsafe_allow_html=True
    )


def display_video(width: int, height: int):
    """Capture and display video streams from RGB & Thermal cameras."""
    video_rgb = cv2.VideoCapture(0)
    video_ther = cv2.VideoCapture(2)
    video_stream = st.empty()

    capture = st.button('📷 Capture', key="capture")

    while video_rgb.isOpened() and video_ther.isOpened() and not capture:
        ret_rgb, frame_rgb = video_rgb.read()
        ret_ther, frame_ther = video_ther.read()

        if ret_rgb:
            frame_rgb = cv2.resize(frame_rgb, (width, height))
            cv2.imwrite(str(RGB_IMG_PATH), frame_rgb)

        if ret_ther:
            frame_ther = cv2.resize(frame_ther, (width, height))
            cv2.imwrite(str(THERMAL_IMG_PATH), frame_ther)

        if ret_ther:
            video_stream.image(frame_ther, channels="BGR")

        if capture:
            break


def display_inputs():
    """Show captured RGB and Thermal images side by side."""
    col1, col2 = st.columns(2)
    with col1:
        st.image(str(THERMAL_IMG_PATH), caption="Thermal Camera", use_column_width=True, channels="BGR")
    with col2:
        st.image(str(RGB_IMG_PATH), caption="RGB Camera", use_column_width=True, channels="BGR")


def run_detection():
    """Run YOLOv7 detection on both Thermal and RGB images."""
    col1, col2 = st.columns(2)

    command_ther = ["python", str(PREDICT_SCRIPT), "--weights", str(THERMAL_WEIGHTS),
                    "--conf", "0.5", "--source", str(THERMAL_IMG_PATH)]
    command_rgb = ["python", str(PREDICT_SCRIPT), "--weights", str(RGB_WEIGHTS),
                   "--conf", "0.25", "--source", str(RGB_IMG_PATH)]

    with col1:
        result_ther = subprocess.run(command_ther, capture_output=True, text=True)
        thermal_output = result_ther.stdout.strip()
        thermal_result_path = Path("seg/runs/predict-seg/exp/tes_thermal.jpg")
        if thermal_result_path.exists():
            st.image(str(thermal_result_path), caption=f"Thermal Detection\n{thermal_output}", use_column_width=True, channels="BGR")

    with col2:
        result_rgb = subprocess.run(command_rgb, capture_output=True, text=True)
        rgb_output = result_rgb.stdout.strip()
        rgb_result_path = Path("seg/runs/predict-seg/exp/tes_rgb.jpg")
        if rgb_result_path.exists():
            st.image(str(rgb_result_path), caption=f"RGB Detection\n{rgb_output}", use_column_width=True, channels="BGR")


# ======================
# MAIN APP
# ======================
def main():
    st.set_page_config(page_title="Bird Detection Dashboard", page_icon="🐦", layout="wide")
    
    set_title()

    # Video Capture Section
    st.header("🎥 Live Capture")
    display_video(NEW_WIDTH, NEW_HEIGHT)

    # Input Images Section
    st.header("📸 Captured Images")
    display_inputs()

    # Detection Section
    if st.button("🚀 Run Detection", key="detect"):
        st.header("📊 Detection Results")
        run_detection()
    else:
        st.info("Click **Run Detection** to process the captured images.")


if __name__ == "__main__":
    main()
