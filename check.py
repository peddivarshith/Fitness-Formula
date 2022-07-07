import streamlit as st
import query as qu
import time
from datetime import date
import smtplib

today = date.today()
today = today.strftime("20%y-%m-%d")
ti = time.strptime(today, "20%y-%m-%d")


def notification(id):
    qu.create_todo_table(id)
    result = qu.read_todo_task(id)
    gmailaddress = '18bd1a05b2@gmail.com'
    gmailpassword = 'rgqfqhrrwvqhenlc'
    mailto = st.session_state.user_email
    SUBJECT = 'Remainder from Fitness Formula..'
    msg = 'Hi user,\nHope you are doing great!! \n\n Here is the list of pending/remainder workouts:\n'
    for i in result:
        print(i)
        ti1 = time.strptime(i[2], "20%y-%m-%d")
        if i[2] == today and i[1] != "Done":
            msg = msg+'- '+i[0]+' exercise Status: ' + \
                i[1] + " and due date by("+i[2] + ") \n"

    print(msg)
    message = 'Subject: {}\n\n{}'.format(SUBJECT, msg)
    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.starttls()
    mailServer.login(gmailaddress, gmailpassword)
    mailServer.sendmail(gmailaddress, mailto, message)
    print(" \n Sent!")
    mailServer.quit()


def About_Us():
    st.markdown('''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <style>
        .fa {
          padding: 20px;
          font-size: 30px;
          width: 150px;
          text-align: center;
          text-decoration: none;
          margin: 5px 2px;
        }
        .fa:hover {
          opacity: 0.7;
        }
        .fa-linkedin {
          background: #007bb5;
          color: white;
        }
        .fa-envelope {
          background: white;
          color: white;
        }
        .fa-github {
          background: #6cc644;
          color: white;
        }
    </style>
    <div><center>
<h1 style="text-align: center;">
<span style="font-size: x-large;">
<u>A</u><u>bout Fitness Formula !</u></span></h1><h3 style="text-align: center;"><span style="font-weight: normal;">
<span style="font-size: large;">Hello Friends Welcome To Fitness Formula</span></span></h3>
<p style="text-align: center;"><br /><p style="font-size: 18px;">
Fitness Formula is a Professional Fitness Platform. Here we not only provide interesting content for exercise, but also enrich the way
the user exercises.<br /><p style="text-align: center;"><br />
<p style="font-size: 18px;">We're dedicated to providing you the best of Fitness,
with a focus on dependability and Fitness for Health Resolution. <br /><br />
<p style="font-size: 18px;">We're working to turn our passion for Fitness into a booming online website. 
We hope you enjoy our Fitness as much as we enjoy offering them to you.</p>
<p style="font-size: 18px;"> Out platform was build based on Pose-Estimation which helps the user from doing wrong way of exercise.</p>
<div style="text-align: center;"><br /></div><div style="text-align: center;"></div><div style="text-align: center;"><h3>Thanks For Visiting Our Site</h3></div><div style="text-align: center;"><a href="" target="_blank"><span style="font-size: medium;"><h4>Contact Us !</h4></span></a></div>
</center></div></br><center> <a href="https://www.linkedin.com/in/sai-varshith-peddi-27150318b/" class="fa fa-linkedin"></a>
<a href="mailto:panduvarshith7562@gmail.com?subject=&cc=cc@example.com" class="fa fa-envelope" aria-hidden="true"></a>
<a href="https://github.com/peddivarshith" class="fa fa-github" aria-hidden="true"></a></center>''', unsafe_allow_html=True)


def Sign_Up():
    st.subheader("Sign Up")
    with st.form(key="form1"):
        first, last = st.columns(2)  # returns container objects

        f_n = first.text_input("First Name")
        l_n = last.text_input("Last Name")
        email, mob = st.columns([3, 1])  # 3:1 ratio size

        user_email = email.text_input("Email ID")
        user_mob = mob.text_input("Mob Number")

        password, repassword = st.columns(2)

        passw = password.text_input("Password", type="password")
        repassw = repassword.text_input("Retype Password", type="password")

        ch, bl, sub = st.columns(3)
        check_box = ch.checkbox("I Agree")

        age = st.slider(label="Choose your age:",
                        min_value=0, max_value=100, value=35)
        weight = st.slider(label="Choose your weight:",
                           min_value=0, max_value=150, value=50)
        submit = st.form_submit_button(label="Submit this form")

        check_mobi = qu.mobilenumber(user_mob)
        check_email = qu.email_id(user_email)
        check_firstname = qu.name(f_n)
        check_lastname = qu.name(l_n)

        if not check_box:
            st.warning("Please agree to the terms and conditions")
        if passw != repassw:
            st.info("The passwords are not matching")
        if not check_mobi:
            st.info("Please Enter the correct Mobile number")
        if not check_email:
            st.info("Please provide your correct email address!")
        if not check_firstname or not check_lastname:
            st.info("Incorrect Name")

        elif check_box and passw == repassw and check_email and check_lastname and check_firstname and check_mobi:
            qu.create_table()
            qu.add_userdata(f_n, l_n, passw, user_email, user_mob, age, weight)
            st.balloons()
            st.success("Account Created Successfully")


def login_details():
    user_email = st.sidebar.text_input("Email ID")
    password, repassword = st.sidebar.columns(2)

    passw = password.text_input("Password", type="password")

    qu.create_table()
    data = qu.login_user(user_email, passw)
    if st.sidebar.checkbox("Login"):
        if data == []:
            st.sidebar.warning('No account found')
            return False
        else:
            st.session_state.user_email = user_email
            st.session_state.password = passw
            st.session_state.id = data[0][7]
            st.sidebar.success("Logged In successfully")
            return True
    return False
