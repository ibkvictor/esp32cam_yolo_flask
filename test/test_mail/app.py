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

    yagmail.register('mce327mce@gmail.com', '327mce327')
    yag = yagmail.SMTP('mce327mce@gmail.com')

    # msg = Message('Hello', sender = 'mce327mce@gmail.com', recipients = ['mce327mce@gmail.com'])
    # msg.body = "Hello Flask message sent from Flask-Mail"
    # mail.send(msg)
    contents = ["This is the body, and here is just text"]
    # This is the body, and here is just text http://somedomain/image.png',
    #         'You can find an audio file attached.', '/local/path/song.mp3']
    yag.send('mce327mce@gmail.com', 'subject', contents)
    return "Sent"

if __name__ == '__main__':
   app.run(debug = True)