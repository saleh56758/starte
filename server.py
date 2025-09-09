# from flask import Flask, render_template, request
# import smtplib
# from email.message import EmailMessage
# from dotenv import load_dotenv
# import os
# from datetime import datetime

# load_dotenv()
# app = Flask(__name__)
# app.secret_key = os.getenv("secret_key")

# OWN_EMAIL = "hassaansaleh56@gmail.com"
# OWN_PASSWORD = "frlb bkff ptwb cwuh"

# @app.context_processor
# def inject_current_year():
#     return {"current_year": datetime.now().year}

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/resume")
# def resume():
#     return render_template("resume.html")

# @app.route("/projects")
# def projects():
#     return render_template("projects.html")

# @app.route("/contact", methods=["GET", "POST"])
# def contact():
#     if request.method == "POST":
#         data = request.form
#         try:
#             send_email(data["name"], data["email"], data["phone"], data["message"])
#             msg_sent = True
#         except Exception as e:
#             print("Failed to send email:", e)
#             msg_sent = False
#         return render_template("contact.html", msg_sent=msg_sent)
#     return render_template("contact.html", msg_sent=None)

# def send_email(name, visitor_email, phone, message):
    
#     email_message = EmailMessage()
#     email_message['Subject'] = "Message from Starte"
#     email_message['From'] = OWN_EMAIL           
#     email_message['To'] = OWN_EMAIL             
#     email_message['Reply-To'] = visitor_email  

#     email_message.set_content(f"""
# Name: {name}
# Email: {visitor_email}
# Phone: {phone}
# Message: {message}
# """)

#     try:
#         with smtplib.SMTP("smtp.gmail.com", 587) as connection:
#             connection.starttls()
#             connection.login(OWN_EMAIL, OWN_PASSWORD)
#             connection.send_message(email_message)
#         print("Email sent successfully")
#     except smtplib.SMTPAuthenticationError as auth_error:
#         print("Authentication failed. Check your App Password:", auth_error)
#     except smtplib.SMTPException as smtp_error:
#         print("SMTP error occurred:", smtp_error)
#     except Exception as e:
#         print("Some other error occurred:", e)

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=8080, debug=True)
from flask import Flask, render_template, request
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
from datetime import datetime
import threading

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("secret_key")

OWN_EMAIL = "hassaansaleh56@gmail.com"
OWN_PASSWORD = "frlb bkff ptwb cwuh"   


@app.context_processor
def inject_current_year():
    return {"current_year": datetime.now().year}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/resume")
def resume():
    return render_template("resume.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        try:
            
            thread = threading.Thread(
                target=send_email,
                args=(data["name"], data["email"], data["phone"], data["message"])
            )
            thread.start()
            msg_sent = True
        except Exception as e:
            print("Failed to start email thread:", e)
            msg_sent = False
        return render_template("contact.html", msg_sent=msg_sent)
    return render_template("contact.html", msg_sent=None)


def send_email(name, visitor_email, phone, message):
    email_message = EmailMessage()
    email_message['Subject'] = "Message from Starte"
    email_message['From'] = OWN_EMAIL
    email_message['To'] = OWN_EMAIL
    email_message['Reply-To'] = visitor_email

    email_message.set_content(f"""
Name: {name}
Email: {visitor_email}
Phone: {phone}
Message: {message}
""")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(OWN_EMAIL, OWN_PASSWORD)
            connection.send_message(email_message)
        print("✅ Email sent successfully")
    except smtplib.SMTPAuthenticationError as auth_error:
        print("❌ Authentication failed. Check your App Password:", auth_error)
    except smtplib.SMTPException as smtp_error:
        print("❌ SMTP error occurred:", smtp_error)
    except Exception as e:
        print("❌ Some other error occurred:", e)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
