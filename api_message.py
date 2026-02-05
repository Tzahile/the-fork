from hashlib import sha256
import hmac
from json import dumps
from os import getenv


class ApiMessage:
    def __init__(
        self,
        action_run_link: str,
        email: str,
        name: str,
        repository_link: str,
        resume_link: str,
        timestamp: str,
    ) -> None:
        self.action_run_link = action_run_link
        self.email = email
        self.name = name
        self.repository_link = repository_link
        self.resume_link = resume_link
        self.timestamp = timestamp

    def to_json(self) -> str:
        payload = {
            "action_run_link": self.action_run_link,
            "email": self.email,
            "name": self.name,
            "repository_link": self.repository_link,
            "resume_link": self.resume_link,
            "timestamp": self.timestamp,
        }
        return dumps(payload, separators=(",", ":"))

    @staticmethod
    def sign_hmac(payload: bytes) -> str:
        private_key = getenv("PRIVATE_KEY")

        return hmac.new(
            private_key.encode("utf-8"),
            payload,
            sha256,
        ).hexdigest()
