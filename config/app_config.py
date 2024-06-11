app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SECRET_KEY"] = "asdfasd"
app.config["UPLOAD_DIR"] = "uploads"

app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '50491de0a0f354'
app.config['MAIL_PASSWORD'] = 'fb25de27c801df'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

app.config['REDIS_URL'] = "redis://default:@localhost:6379/0"