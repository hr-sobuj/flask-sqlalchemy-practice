from flask_mail import Mail

mail=Mail()

def mail_init(app):
    mail.init_app(app)