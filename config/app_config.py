class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///project.db"
    SECRET_KEY = "asdfasd"
    UPLOAD_DIR = "uploads"
    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = '50491de0a0f354'
    MAIL_PASSWORD = 'fb25de27c801df'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    REDIS_URL = "redis://default:@localhost:6379/0"

    PROPAGATE_EXCEPTIONS = True
    API_TITLE = "Blog REST API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
