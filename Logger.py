from datetime import datetime

class Logger:

    #Z założenia INFO to komunikaty, które można pominąć, WARNING to takie, które wymagają uwagi lub reakcji, a ERROR to komunikaty błędów.
    COLORS = {
        "INFO": "",  # Domyślny
        "WARNING": "\033[33m",  # Pomarańczowy
        "ERROR": "\033[31;1m"  # Czerwony pogrubiony
    }
    RESET_COLOR = "\033[0m"
    LOG_FILE = "logs.txt"
    CLEAR_LOGS_ON_START = True

    def __init__(self):
        if self.CLEAR_LOGS_ON_START:
            self._clear_log_file()

    def log(self, level, message):
        if level not in ["INFO", "WARNING", "ERROR"]:
            raise ValueError(f"Invalid log level: {level}")

        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S:%f")[:-3]
        raw_message = f"[{level} {timestamp}] {message}"

        formatted_message = f"{self.COLORS[level]}{raw_message}{self.RESET_COLOR}"
        print(formatted_message)

        self._write_to_file(raw_message)

    def _write_to_file(self, message):
        with open(self.LOG_FILE, "a") as log_file:
            log_file.write(message + "\n")

    def _clear_log_file(self):
        with open(self.LOG_FILE, "w") as log_file:
            log_file.write("")
