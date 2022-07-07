import time
import datetime
import smtplib
gmailaddress = '18bd1a05b2@gmail.com'
gmailpassword = 'rgqfqhrrwvqhenlc'
mailto = 'peddivarshith292000@gmail.com'
SUBJECT = 'Todays present'
msg = 'sankar is present today'
message = 'Subject: {}\n\n{}'.format(SUBJECT, msg)
mailServer = smtplib.SMTP('smtp.gmail.com', 587)
mailServer.starttls()
mailServer.login(gmailaddress, gmailpassword)
mailServer.sendmail(gmailaddress, mailto, message)
print(" \n Sent!")
mailServer.quit()
