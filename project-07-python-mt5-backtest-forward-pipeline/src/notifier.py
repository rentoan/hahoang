import json
import urllib.request

class TelegramNotifier:
    def __init__(self, token=None, chat_id=None):
        self.token = token
        self.chat_id = chat_id

    def enabled(self):
        return bool(self.token and self.chat_id)

    def send(self, message):
        if not self.enabled():
            print("[TELEGRAM DISABLED]", message)
            return

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = json.dumps({
            "chat_id": self.chat_id,
            "text": message
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=15) as response:
            response.read()
