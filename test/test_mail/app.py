from flask import Flask
# from flask_mail import Mail, Message
import yagmail

app = Flask(__name__)
# mail= Mail(app)

# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'mce327mce@gmail.com'
# app.config['MAIL_PASSWORD'] = '327mce327'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# mail = Mail(app)



@app.route("/")
def index():
    sender_email_address = input("enter recipients email address:   ")
    sender_password = input("enter recipients email address:    ")
    yagmail.register(sender_email_address, sender_password)
    recipient_email_address = input("enter recipients email address:    ")
    yag = yagmail.SMTP(sender_email_address)

    # msg = Message('Hello', sender = '****************e@gmail.com', recipients = ['************@gmail.com'])
    # msg.body = "Hello Flask message sent from Flask-Mail"
    # mail.send(msg)
    contents = ["This is the body, and here is just text"]
    # This is the body, and here is just text http://somedomain/image.png',
    #         'You can find an audio file attached.', '/local/path/song.mp3']
    yag.send(recipient_email_address, 'subject', contents)
    return "Sent"

if __name__ == '__main__':
   app.run(debug = True)