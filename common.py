import logging
from dotenv import load_dotenv
from os import getenv

load_dotenv()

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BLUE = "\033[94m"


class ColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_message = super().format(record)
        level_name = record.levelname  # Log darajasini olish
        if record.levelno == logging.DEBUG:
            return f"{BLUE}[{level_name}] {log_message}{RESET}"
        elif record.levelno == logging.INFO:
            return f"{GREEN}[{level_name}] {log_message}{RESET}"
        elif record.levelno == logging.WARNING:
            return f"{YELLOW}[{level_name}] {log_message}{RESET}"
        elif record.levelno >= logging.ERROR:
            return f"{RED}[{level_name}] {log_message}{RESET}"
        return f"[{level_name}] {log_message}"


# Logger sozlash
handler = logging.StreamHandler()
handler.setFormatter(
    ColorFormatter(
        "\nTime: %(asctime)s \nFile: %(filename)s:%(lineno)d \nMessage: %(message)s"
    )
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

ADMIN_ID = getenv("ADMIN_ID")
if not ADMIN_ID:
    raise ValueError('Admin id not found')
ADMIN_ID = int(ADMIN_ID)

BOT_USERNAME= getenv("BOT_USERNAME")
if not ADMIN_ID:
    raise ValueError('BOT_USERNAME not found')
SECRET_KEY= getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError('SECRET_KEY not found')
