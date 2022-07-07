import streamlit as st
from streamlit_option_menu import option_menu
import check as ck
import mediapipe as mp
from pandas import DataFrame
from numpy import array
from matplotlib.pyplot import plot
import plotly.graph_objs as go
from logic_functions import local_css, display_content
from Back import Bird_Dog, Superman_Y, Superman_T
from Back_Upper_Arm import Tricep_Dip_1, Bent_Over_Tricep, Overhead_Tricep, Tricep_Dip_2
from Chest import Plank_Jacks, Incline_Pushup, Push_Up
from Front_Upper_Arm import Wide_Curl, Hammer_Curl, Bicep_Curl, Dumbbell_Workout_Left_Arm, Dumbbell_Workout_Right_Arm
from Lunge import Lateral_Lunge, Reverse_Lunge
from Neck import Neck_Extension, Neck_Stretch
from Leg import Calf_Raises, Donkey_Kicks, High_Knees
from Shoulders import Triangle_Push_Up, Shoulder_Military_Press, Plank_Up_Down
from Squats import Dumbbell_DeadLift_Squats, Sumo_Squats, Jump_Squats
import query as qu
from todo_app import remainder

# import gc

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
st.set_page_config(page_title='Fitness Formula', page_icon='Images/logo.gif',
                   layout='wide', initial_sidebar_state='auto')

# to remove tab name and top right menu option and footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# -----------------------------------------------------------

st.set_option('deprecation.showfileUploaderEncoding', False)
st.set_option('deprecation.showPyplotGlobalUse', False)

st.markdown("<center><h1>Fitness Formula</h1></center>",
            unsafe_allow_html=True)
# Authentication
st.sidebar.image("Images/logo.gif")
user = st.sidebar.selectbox(
    "About Us", ["Why Fitness Formula?", "Sign Up", "Login"])
if user == 'Why Fitness Formula?':

    ck.About_Us()

elif user == 'Sign Up':
    ck.Sign_Up()

else:
    value = ck.login_details()
    if value:
        ck.notification(st.session_state.id)
        print(st.session_state.user_email)

        if st.sidebar.checkbox("ToDoList"):
            remainder(st.session_state.id)

        elif st.sidebar.checkbox("Performance Results"):
            selected = option_menu(
                menu_title=None,
                options=["History of Workout",
                         "Trace of Workout", "Complete Record"],
                icons=['bar-chart-fill', 'graph-up', 'clipboard-data'],
                default_index=0,
                orientation="horizontal"
            )
            if selected == "History of Workout":

                st.markdown(
                    "<h1 style='text-align: center; color: white;'>History of Workout</h1>", unsafe_allow_html=True)
                Exercise_type = ["Back Exercises", "Back of Upper Arm Exercises", "Chest Exercises", "Front of Upper Arm Exercises", "Lunge Exercises",
                                 "Neck Exercises", "Leg Exercises", "Shoulders Exercises", "Squats Exercises"]
                select = st.selectbox(
                    "Choose Exercise Type", Exercise_type, index=0)
                data = qu.query_workout_data(st.session_state.id, select)
                data = DataFrame(data, columns=(
                    "Exercise Name", "Number of Times"))
                how_to_display_data = st.radio(
                    "Represent Data as", ["Table", "Bar Chart"], index=0)
                if(how_to_display_data == "Table"):
                    st.table(data)
                else:
                    trace = go.Bar(
                        x=data["Exercise Name"], y=data["Number of Times"], showlegend=True)
                    layout = go.Layout(title=select)
                    data1 = [trace]
                    fig = go.Figure(data=data1, layout=layout)
                    st.plotly_chart(fig, use_container_width=True)

            elif selected == "Trace of Workout":
                st.markdown(
                    "<h1 style='text-align: center; color: white;'>Trace of Workout</h1>", unsafe_allow_html=True)
                trace = array(qu.trace_workout_date(st.session_state.id))
                st.markdown(
                    "<h3 style='text-align: center; color: white;'>Date vs Number of TimesSome title</h3>", unsafe_allow_html=True)
                print(trace)
                if trace != []:
                    plot(trace[:, 0], trace[:, 1], 'xb-')
                st.pyplot()

            elif selected == "Complete Record":

                st.markdown(
                    "<h1 style='text-align: center; color: white;'>Complete Record</h1>", unsafe_allow_html=True)
                data = qu.send_workout_data(st.session_state.id)
                data = DataFrame(
                    data, columns=['Date', 'Exercise Type', 'Exercise Name', 'Number of Times'])
                st.download_button(
                    "Download as CSV",
                    data.to_csv().encode('utf-8'),
                    "Record.csv",
                    "text/csv",
                    key='download-csv'

                )
                st.table(data)

        else:
            type_of_exercies = st.sidebar.selectbox("Choose your WorkOut",
                                                    ["Todays news", "Back Exercises", "Back of Upper Arm Exercises",
                                                     "Chest Exercises",
                                                     "Front of Upper Arm Exercises", "Lunge Exercises", "Neck Exercises",

                                                     "Leg Exercises", "Shoulders Exercises", "Squats Exercises"])

            if 'counter' not in st.session_state:
                st.session_state.counter = 0
                st.session_state.sub_type = None

            if type_of_exercies == "Todays news":
                st.title("Display Todays news")

            elif type_of_exercies == "Back Exercises":
                type_of_back = st.sidebar.selectbox("Choose your Back WorkOut",
                                                    ["None", "Bird Dog", "Superman T", "Superman Y"])

                if st.session_state.counter != 0:
                    qu.workout_data(st.session_state.id, "Back Exercises",
                                    st.session_state.sub_type, st.session_state.counter)
                    st.session_state.counter = 0

                if type_of_back == "Bird Dog":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Bird Dog"
                        Bird_Dog()

                    else:
                        display_content("Back_Exercises", "Bird Dog")

                elif type_of_back == "Superman T":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Superman T"
                        Superman_T()
                    else:
                        display_content("Back_Exercises", "Superman T")

                elif type_of_back == "Superman Y":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Superman Y"
                        Superman_Y()
                    else:
                        display_content("Back_Exercises", "Superman Y")

                else:
                    st.write('Display what is Back Exercises')

            elif type_of_exercies == "Back of Upper Arm Exercises":

                type_of_back_upper_arm = st.sidebar.selectbox("Choose your Back Upper Arm WorkOut",
                                                              ["None", "Bent Over Tricep", "Overhead Tricep",
                                                               "Tricep Dip 1",
                                                               "Tricep Dip 2"])

                if st.session_state.counter != 0:
                    # store in database
                    st.session_state.counter = 0
                    st.session_state.sub_type = None

                if type_of_back_upper_arm == "Bent Over Tricep":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Bent Over Tricep"
                        Bent_Over_Tricep()
                    else:
                        display_content(
                            "Back_of_Upper_Arm_Exercises", "Bent Over Tricep")

                elif type_of_back_upper_arm == "Overhead Tricep":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Overhead Tricep"
                        Overhead_Tricep()
                    else:
                        display_content(
                            "Back_of_Upper_Arm_Exercises", "Overhead Tricep")

                elif type_of_back_upper_arm == "Tricep Dip 1":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Tricep Dip 1"
                        Tricep_Dip_1()
                    else:
                        display_content(
                            "Back_of_Upper_Arm_Exercises", "Tricep Dip 1")

                elif type_of_back_upper_arm == "Tricep Dip 2":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Tricep Dip 2"
                        Tricep_Dip_2()
                    else:
                        display_content(
                            "Back_of_Upper_Arm_Exercises", "Tricep Dip 2")

                else:
                    st.write('Display what is Back Upper Arm Exercises')

            elif type_of_exercies == "Chest Exercises":

                type_of_chest = st.sidebar.selectbox("Choose your Chest WorkOut",
                                                     ["None", "Incline Pushup", "Plank Jacks", "Push Up"])

                if st.session_state.counter != 0:
                    # store in database
                    st.session_state.counter = 0
                    st.session_state.sub_type = None

                if type_of_chest == "Incline Pushup":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Incline Pushup"
                        Incline_Pushup()
                    else:
                        display_content("Chest_Exercises", "Incline Pushup")

                elif type_of_chest == "Plank Jacks":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Plank Jacks"
                        Plank_Jacks()
                    else:
                        display_content("Chest_Exercises", "Plank Jacks")

                elif type_of_chest == "Push Up":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Push Up"
                        Push_Up()
                    else:
                        display_content("Chest_Exercises", "Push Up")

                else:
                    st.write('Display what is Chest Exercises')

            elif type_of_exercies == "Front of Upper Arm Exercises":

                type_of_front_upper_arm = st.sidebar.selectbox("Choose your Front Upper Arm WorkOut",
                                                               ["None", "Dumbbell Workout Left Arm", "Dumbbell Workout "
                                                                                                     "Right Arm",
                                                                "Bicep Curl", "Hammer Curl", "Wide Curl"])

                if st.session_state.counter != 0:
                    # store in database
                    st.session_state.counter = 0
                    st.session_state.sub_type = None

                if type_of_front_upper_arm == "Dumbbell Workout Left Arm":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Dumbbell Workout Left Arm"
                        Dumbbell_Workout_Left_Arm()
                    else:
                        display_content(
                            "Front_of_Upper_Arm_Exercises", "Dumbbell Workout Left Arm")

                elif type_of_front_upper_arm == "Dumbbell Workout Right Arm":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Dumbbell Workout Right Arm"
                        Dumbbell_Workout_Right_Arm()
                    else:
                        display_content(
                            "Front_of_Upper_Arm_Exercises", "Dumbbell Workout Right Arm")

                elif type_of_front_upper_arm == "Bicep Curl":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Bicep Curl"
                        Bicep_Curl()
                    else:
                        display_content(
                            "Front_of_Upper_Arm_Exercises", "Bicep Curl")

                elif type_of_front_upper_arm == "Hammer Curl":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Hammer Curl"
                        Hammer_Curl()
                    else:
                        display_content(
                            "Front_of_Upper_Arm_Exercises", "Hammer Curl")

                elif type_of_front_upper_arm == "Wide Curl":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Wide Curl"
                        Wide_Curl()
                    else:
                        display_content(
                            "Front_of_Upper_Arm_Exercises", "Wide Curl")

                else:
                    st.write('Display what is Front Upper Arm Exercises')

            elif type_of_exercies == "Lunge Exercises":

                type_of_Lunge = st.sidebar.selectbox("Choose your Lunge WorkOut",
                                                     ["None", "Lateral Lunge", "Reverse Lunge"])

                if st.session_state.counter != 0:
                    # store in database
                    st.session_state.counter = 0
                    st.session_state.sub_type = None

                if type_of_Lunge == "Lateral Lunge":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Lateral Lunge"
                        Lateral_Lunge()
                    else:
                        display_content("Lunge_Exercises", "Lateral Lunge")

                elif type_of_Lunge == "Reverse Lunge":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Reverse Lunge"
                        Reverse_Lunge()
                    else:
                        display_content("Lunge_Exercises", "Reverse Lunge")

                else:
                    st.title('Display what is Lunge Exercises')

            elif type_of_exercies == "Neck Exercises":

                type_of_neck = st.sidebar.selectbox("Choose your Neck WorkOut", [
                                                    "None", "Neck Extension", "Neck Stretch"])

                if st.session_state.counter != 0:
                    # store in database
                    st.session_state.counter = 0
                    st.session_state.sub_type = None

                if type_of_neck == "Neck Extension":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Neck Extension"
                        Neck_Extension()
                    else:
                        display_content("Neck_Exercises", "Neck Extension")

                elif type_of_neck == "Neck Stretch":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Neck Stretch"
                        Neck_Stretch()
                    else:
                        display_content("Neck_Exercises", "Neck Stretch")

                else:
                    st.title('Display what is Neck Exercises')

            elif type_of_exercies == "Leg Exercises":

                type_of_leg = st.sidebar.selectbox("Choose your Leg WorkOut",
                                                   ["None", "Calf Raises", "Donkey Kicks", "High Knees"])

                if st.session_state.counter != 0:
                    # store in database
                    st.session_state.counter = 0
                    st.session_state.sub_type = None

                if type_of_leg == "Calf Raises":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Calf Raises"
                        Calf_Raises()
                    else:
                        display_content("Other_Leg_Exercises", "Calf Raises")

                elif type_of_leg == "Donkey Kicks":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Donkey Kicks"
                        Donkey_Kicks()
                    else:
                        display_content("Other_Leg_Exercises", "Donkey Kicks")

                elif type_of_leg == "High Knees":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "High Knees"
                        High_Knees()
                    else:
                        display_content("Other_Leg_Exercises", "High Knees")

                else:
                    st.title('Display what is Leg Exercises')

            elif type_of_exercies == "Shoulders Exercises":
                type_of_shoulder = st.sidebar.selectbox("Choose your Shoulder WorkOut",
                                                        ["None", "Plank Up Down", "Shoulder Military Press",
                                                         "Triangle Push Ups"])

                if st.session_state.counter != 0:
                    # store in database
                    st.session_state.counter = 0
                    st.session_state.sub_type = None

                if type_of_shoulder == "Plank Up Down":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Plank Up Down"
                        Plank_Up_Down()
                    else:
                        display_content("Shoulders_Exercise", "Plank Up Down")

                elif type_of_shoulder == "Shoulder Military Press":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Shoulder Military Press"
                        Shoulder_Military_Press()
                    else:
                        display_content("Shoulders_Exercise",
                                        "Shoulder Military Press")

                elif type_of_shoulder == "Triangle Push Ups":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Triangle Push Ups"
                        Triangle_Push_Up()
                    else:
                        display_content("Shoulders_Exercise",
                                        "Triangle Push Ups")

                else:
                    st.title('Display what is shoulder Exercises')

            elif type_of_exercies == "Squats Exercises":
                type_of_squats = st.sidebar.selectbox("Choose your Squat WorkOut",
                                                      ["None", "Dumbbell DeadLift Squats", "Jump Squats", "Sumo Squats"])

                if st.session_state.counter != 0:
                    # store in database
                    st.session_state.counter = 0
                    st.session_state.sub_type = None

                if type_of_squats == "Dumbbell DeadLift Squats":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Dumbbell DeadLift Squats"
                        Dumbbell_DeadLift_Squats()
                    else:
                        display_content("Squats_Exercises",
                                        "Dumbbell DeadLift Squats")

                elif type_of_squats == "Jump Squats":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Jump Squats"
                        Jump_Squats()
                    else:
                        display_content("Squats_Exercises", "Jump Squats")

                elif type_of_squats == "Sumo Squats":
                    if st.sidebar.button("Start", key="1"):
                        st.session_state.counter = 0
                        st.session_state.sub_type = "Sumo Squats"
                        Sumo_Squats()
                    else:
                        display_content("Squats_Exercises", "Sumo Squats")
                else:
                    st.title('Display what is squats Exercises')
    else:
        st.sidebar.warning("Please fill the details")
