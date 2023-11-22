import streamlit as st
import cv2

# dev = "0"
new_width = 640
new_height = 480

def title():
    center_style = """
    <style>
    .center {
        display: flex;
        justify-content: center;
        text-align: center;
    }
    </style>
    """
    # Display the centered text
    st.markdown(center_style, unsafe_allow_html=True)
    st.markdown("<div class='center'><h1>Bird Counter and Detector Dashboard</h1></div>", unsafe_allow_html=True)

def display_video(new_width, new_height):
    video0 = cv2.VideoCapture(0)
    video1 = cv2.VideoCapture(3)
    video_stream = st.empty()
    capture_button = st.button('Capture', key=1)
    while video0.isOpened and video1.isOpened and not capture_button:
        ret0, frame0 = video0.read()
        ret1, frame1 = video1.read()
        if not ret0 and not ret1:
            break
        # frame_rgb  = cv2.resize(frame0, (new_width, new_height))
        # frame_ther = cv2.resize(frame1, (new_width, new_height))
        # frame_rgb = cv2.cvtColor(frame_rgb, cv2.COLOR_BGR2RGB)
        # frame_ther = cv2.cvtColor(frame_ther, cv2.COLOR_BGR2RGB)
        video_stream.image(frame0, channels="RGB")
        cv2.imwrite('tes_2rgb.jpg', frame0)
        cv2.imwrite('tes_2ther.jpg', frame1)
        if capture_button:  # If the 'Capture' button is clicked
            # cv2.imwrite('tes_rgb.jpg', frame_rgb)
            # cv2.imwrite('tes_ther.jpg', frame_ther)
            break
        
    
    
        
def output():
    thermal = cv2.imread("tes_2ther.jpg")
    # thermal = cv2.cvtColor(thermal, cv2.COLOR_BGR2RGB)
    rgb = cv2.imread("tes_2rgb.jpg")
    # rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
    tab_1, tab_2 = st.columns(2)
    with tab_1:
        st.image(thermal, use_column_width=True, caption='Thermal')
    with tab_2:
        st.image(rgb, use_column_width=True, caption='RGB')
        
    

def detect():
    thermal = cv2.imread("tes_2ther.jpg")
    thermal = cv2.cvtColor(thermal, cv2.COLOR_BGR2RGB)
    rgb = cv2.imread("tes_2ther.jpg")
    rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
    ta_1, ta_2 = st.columns(2)
    with ta_1:
        st.image(thermal, use_column_width=True, caption='Thermal')
    with ta_2:
        st.image(rgb, use_column_width=True, caption='RGB')

def main():
    st.set_page_config(
        page_title="Dashboard",
        page_icon="🧊",
        # layout="wide",
        initial_sidebar_state="expanded"
    )
    # Title
    title()
    display_video(new_width, new_height)
    # Stream Video
    with st.container():
        st.header("Input Image")
        output()
    peace_holder = st.empty()
    detect_button = st.button("Detect", key=2)
    while not detect_button:
        peace_holder.header("Result") 
        if detect_button:
            break
    st.header("Result") 
    detect()

if __name__ == "__main__":
    main()