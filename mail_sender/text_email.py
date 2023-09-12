import smtplib
import ssl

# Setup port number and servr name

smtp_port = 587                 # Standard secure SMTP port
smtp_server = "smtp.gmail.com"  # Google SMTP Server


# Set up the email lists
email_from = "booksmartapp358@gmail.com"
email_list = ["p.uryga@gmail.com", "kreative358@gmail.com", "kreative358@hotmail.com"]
email_to = "p.uryga@gmail.com"

# Define the password (better to reference externally)
pswd = "ikzliaiijzdvbqlq" # As shown in the video this password is now dead, left in as example only

subject = "New email from TIE with attachments!!"
message = "Dear lord, please help !!!"
simple_email_context = ssl.create_default_context()

try:
    print("Connecting to server...")
    TIE_server = smtplib.SMTP(smtp_server, smtp_port)
    TIE_server.starttls(context=simple_email_context)
    TIE_server.login(email_from, pswd)
    print("Connecting to server OK")

    print()
    print(f"Sending email to - {email_to}")
    TIE_server.sendmail(email_from, email_to, subject, message)
    print(f"Email successfully sent to - {email_to}")

except Exception as e:
    print(e)

finally:
    TIE_server.quit()

# name the email subject
subject = "New email from TIE with attachments!!"

# Define the email function (dont call it email!)
def send_emails(email_list):

    for person in email_list:

        # Make the body of the email
        body = f"""
        line 1
        line 2
        line 3
        etc
        """

        # make a MIME object to define parts of the email
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = person
        msg['Subject'] = subject

        # Attach the body of the message
        msg.attach(MIMEText(body, 'plain'))

        # Define the file to attach
        filename = "random_data.csv"

        # Open the file in python as a binary
        attachment= open(filename, 'rb')  # r for read and b for binary

        # Encode as base 64
        attachment_package = MIMEBase('application', 'octet-stream')
        attachment_package.set_payload((attachment).read())
        encoders.encode_base64(attachment_package)
        attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename)
        msg.attach(attachment_package)

        # Cast as string
        text = msg.as_string()

        # Connect with the server
        print("Connecting to server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls()
        TIE_server.login(email_from, pswd)
        print("Succesfully connected to server")
        print()

        # Send emails to "person" as list is iterated
        print(f"Sending email to: {person}...")
        TIE_server.sendmail(email_from, person, text)
        print(f"Email sent to: {person}")
        print()

    # Close the port
    TIE_server.quit()


# Run the function
send_emails(email_list)