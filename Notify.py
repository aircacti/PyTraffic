import os
from plyer import notification
import time


class Notify:
    last_alert_time = 0

    @staticmethod
    def alert():
        current_time = time.time()

        if current_time - Notify.last_alert_time >= 10:
            notification.notify(
                title="Niebezpieczne połączenie",
                message=f"Opuść otwartą stronę!",
                timeout=5,
                app_icon=os.path.join(os.getcwd(), 'ico.ico')
            )

            Notify.last_alert_time = current_time

