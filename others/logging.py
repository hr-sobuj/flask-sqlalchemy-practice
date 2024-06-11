log_level = logging.DEBUG
log_file = "app.log"
log_format = "%(asctime)s - %(levelname)s - %(message)s"
log_mode = "a"

logging.basicConfig(
    filename=log_file, filemode=log_mode, format=log_format, level=log_level
)

