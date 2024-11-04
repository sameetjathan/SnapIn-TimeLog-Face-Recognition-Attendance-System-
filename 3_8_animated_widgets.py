import smtplib
from email.mime.text import MIMEText

sender_email = "soham56kadam@gmail.com"
receiver_email = "soham56kadam@gmail.com"
app_password = "nbri nljt jiqk adsy"  # This should be the 16-character app password generated from Google, not your Google password

# Create MIMEText object for a properly formatted email
message = MIMEText('This is the body of the email')
message['Subject'] = 'SENDDDDD'
message['From'] = sender_email
message['To'] = receiver_email

# Connect to the Gmail SMTP server and send the email
server = smtplib.SMTP('smtp.gmail.com', 587)  # Correct server and port
server.starttls()  # Start TLS encryption
server.login(sender_email, app_password)  # Log in to the server
server.sendmail(sender_email, receiver_email, message.as_string())  # Send the email
server.quit()  # Log out from the server
print('Mail sent successfully')
