import streamlit as st
import cv2
from numpy import array, dot, linalg, arccos, degrees
import json
import base64


def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)


@st.cache()
def calculate_angle(a, b, c):
    a = array(a)  # First
    b = array(b)  # Mid
    c = array(c)  # End

    # radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    # angle = np.abs(radians * 180.0 / np.pi)
    #
    # if angle > 180.0:
    #     angle = 360 - angle
    #
    # return angle
    ba = a - b
    bc = c - b
    cosine_angle = dot(ba, bc) / (linalg.norm(ba) * linalg.norm(bc))
    angle = arccos(cosine_angle)

    return degrees(angle)


@st.cache()
def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


def display_content(exercise, workout):
    f = open("Load/" + exercise + ".json")
    load_data = json.load(f)
    file_ = open(load_data[workout]["Exercise_Image"], "rb")

    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    st.markdown(
        f'<center><img width="600" height="400" src="data:image/gif;base64,{data_url}"></center>',
        unsafe_allow_html=True,
    )
    local_css("style.css")
    print_data = (str)(load_data[workout]["Exercise_Content"])
    st.markdown("<div class='highlight red'><span class='bold'>" + print_data + "</span></div>",
                unsafe_allow_html=True)


