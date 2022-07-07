import streamlit as st
import mediapipe as mp
import cv2
import random as r
from logic_functions import calculate_angle, image_resize

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

ret = None;frame = None;image = None;results = None;landmarks = None;
wrist_r = None;wrist_l = None;shoulder_r = None;shoulder_l = None;knee_l = None;ankle_l = None;ankle_r = None;
hip_l = None;hip_r = Noneelbow_r = None;elbow_l = None;knee_r = None;elbow_r = None;
angle = None;angle1 = None;angle2 = None;angle3 = None;angle4 = None;foot_index_l = None;foot_index_r = None

def High_Knees():
    cap = cv2.VideoCapture(0)

    FRAME_WINDOW = st.image([])

    stage = "Right"
    kpi1, kpi2 = st.sidebar.columns(2)
    kpi3, kpi4 = st.sidebar.columns(2)

    with kpi1:
        st.sidebar.markdown("**Rip's Count**")
        kpi1_text = st.sidebar.markdown("0")
    with kpi2:
        st.sidebar.markdown("**Position**")
        kpi2_text = st.sidebar.markdown("0")

    with kpi3:
        st.sidebar.markdown("**Right Knee**")
        kpi3_text = st.sidebar.markdown("0")

    with kpi4:
        st.sidebar.markdown("**Left Knee**")
        kpi4_text = st.sidebar.markdown("0")

    b1 = st.button("Stop", key=r.randint(1, 100000))
    if b1:
        cap.release()
        cv2.destroyAllWindows()
        return

    st.markdown("<hr/>", unsafe_allow_html=True)
    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates

                knee_l = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                knee_r = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

                ankle_l = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                ankle_r = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                hip_l = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                hip_r = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

                shoulder_r = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                shoulder_l = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

                elbow_r = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                elbow_l = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]

                # Calculate angle
                angle1 = calculate_angle(hip_l, shoulder_l, elbow_l)
                angle2 = calculate_angle(hip_r, shoulder_r, elbow_r)
                angle3 = calculate_angle(hip_l, knee_l, ankle_l)
                angle4 = calculate_angle(hip_r, knee_r, ankle_r)

                # Curl counter logic
                if angle1 <= 90 and angle3 <= 110 and stage == "Right":
                    stage = "Left"
                    st.session_state.counter += 0.5
                if angle2 <= 90 and angle4 <= 110 and stage == "Left":
                    stage = "Right"
                    st.session_state.counter += 0.5
                    print(st.session_state.counter)

                kpi1_text.write(f"<h1 style='text-align: center; color: red;'>{st.session_state.counter}</h1>",
                                unsafe_allow_html=True)

                kpi2_text.write(f"<h1 style='text-align: center; color: red;'>{stage}</h1>",
                                unsafe_allow_html=True)

                kpi3_text.write(f"<h1 style='text-align: center; color: red;'>{round(angle4, 2)}</h1>",
                                unsafe_allow_html=True)

                kpi4_text.write(f"<h1 style='text-align: center; color: red;'>{round(angle3, 2)}</h1>",
                                unsafe_allow_html=True)


            except:
                pass

            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )

            # Displaying out pose
            image = cv2.resize(image, (0, 0), fx=0.8, fy=0.8)
            image = image_resize(image=image, height=1000)
            FRAME_WINDOW.image(image, channels='BGR')
        del ret, frame, image, results, landmarks, wrist_r, wrist_l
        del shoulder_r, shoulder_l, hip_l, hip_r, elbow_l, elbow_r, knee_r, angle2, angle1, angle3

        cap.release()
        cv2.destroyAllWindows()
        return


def Donkey_Kicks():
    cap = cv2.VideoCapture(0)

    FRAME_WINDOW = st.image([])

    stage = "Unlift"
    kpi1, kpi2, kpi3 = st.sidebar.columns(3)

    with kpi1:
        st.sidebar.markdown("**Rip's Count**")
        kpi1_text = st.sidebar.markdown("0")
    with kpi2:
        st.sidebar.markdown("**Position**")
        kpi2_text = st.sidebar.markdown("0")

    with kpi3:
        st.sidebar.markdown("**Right Hip**")
        kpi3_text = st.sidebar.markdown("0")

    b1 = st.button("Stop", key=r.randint(1, 100000))
    if b1:
        cap.release()
        cv2.destroyAllWindows()
        return

    st.markdown("<hr/>", unsafe_allow_html=True)
    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates

                shoulder_r = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                hip_r = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

                knee_r = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

                # Calculate angle
                angle = calculate_angle(shoulder_r, hip_r, knee_r)

                # Curl counter logic
                if angle <= 110 and stage == "Unlift":
                    stage = "Lift"
                    st.session_state.counter += 0.5
                if angle >= 170 and stage == "Lift":
                    stage = "Unlift"
                    st.session_state.counter += 0.5
                    print(st.session_state.counter)

                kpi1_text.write(f"<h1 style='text-align: center; color: red;'>{st.session_state.counter}</h1>",
                                unsafe_allow_html=True)

                kpi2_text.write(f"<h1 style='text-align: center; color: red;'>{stage}</h1>",
                                unsafe_allow_html=True)

                kpi3_text.write(f"<h1 style='text-align: center; color: red;'>{round(angle, 2)}</h1>",
                                unsafe_allow_html=True)

            except:
                pass

            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )

            # Displaying out pose
            image = cv2.resize(image, (0, 0), fx=0.8, fy=0.8)
            image = image_resize(image=image, height=1000)
            FRAME_WINDOW.image(image, channels='BGR')
        del ret, frame, image, results, landmarks, wrist_r, wrist_l
        del shoulder_r, shoulder_l, hip_l, hip_r, elbow_l, elbow_r, knee_r, angle2, angle1, angle3

        cap.release()
        cv2.destroyAllWindows()
        return


def Calf_Raises():
    cap = cv2.VideoCapture(0)

    FRAME_WINDOW = st.image([])

    stage = "Unlift"
    kpi1, kpi2 = st.sidebar.columns(2)
    kpi3, kpi4 = st.sidebar.columns(2)

    with kpi1:
        st.sidebar.markdown("**Rip's Count**")
        kpi1_text = st.sidebar.markdown("0")
    with kpi2:
        st.sidebar.markdown("**Position**")
        kpi2_text = st.sidebar.markdown("0")

    with kpi3:
        st.sidebar.markdown("**Ankle Left**")
        kpi3_text = st.sidebar.markdown("0")

    with kpi4:
        st.sidebar.markdown("**Ankle Right**")
        kpi4_text = st.sidebar.markdown("0")

    b1 = st.button("Stop", key=r.randint(1, 100000))
    if b1:
        cap.release()
        cv2.destroyAllWindows()
        return

    st.markdown("<hr/>", unsafe_allow_html=True)
    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates

                knee_l = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                knee_r = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

                ankle_l = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                ankle_r = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                foot_index_l = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
                foot_index_r = [landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x,
                                landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]

                # Calculate angle
                angle1 = calculate_angle(knee_l, ankle_l, foot_index_l)
                angle2 = calculate_angle(knee_r, ankle_r, foot_index_r)

                # Curl counter logic
                if angle1 <= 130 and angle2 <= 130 and stage == "Unlift":
                    stage = "Lift"
                    st.session_state.counter += 0.5
                if angle1 >= 150 and angle2 >= 150 and stage == "Lift":
                    stage = "Unlift"
                    st.session_state.counter += 0.5
                    print(st.session_state.counter)

                kpi1_text.write(f"<h1 style='text-align: center; color: red;'>{st.session_state.counter}</h1>",
                                unsafe_allow_html=True)

                kpi2_text.write(f"<h1 style='text-align: center; color: red;'>{stage}</h1>",
                                unsafe_allow_html=True)

                kpi3_text.write(f"<h1 style='text-align: center; color: red;'>{round(angle1, 2)}</h1>",
                                unsafe_allow_html=True)

                kpi4_text.write(f"<h1 style='text-align: center; color: red;'>{round(angle2, 2)}</h1>",
                                unsafe_allow_html=True)


            except:
                pass

            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )

            # Displaying out pose
            image = cv2.resize(image, (0, 0), fx=0.8, fy=0.8)
            image = image_resize(image=image, height=1000)
            FRAME_WINDOW.image(image, channels='BGR')
        del ret, frame, image, results, landmarks, wrist_r, wrist_l
        del shoulder_r, shoulder_l, hip_l, hip_r, elbow_l, elbow_r, knee_r, angle2, angle1, angle3

        cap.release()
        cv2.destroyAllWindows()
        return
