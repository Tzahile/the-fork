from datetime import datetime, timezone
from os import getenv
from sys import stderr
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import json

from api_message import ApiMessage

API_URL = "https://b12.io/apply/submission"


def get_iso8601() -> str:
    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()
    return now_iso.replace("+00:00", "Z")


def main() -> int:
    if not getenv("PRIVATE_KEY"):
        print("private key is missing", file=stderr)
        return 2

    # create data
    message = ApiMessage(
        action_run_link="https://link-to-github-or-another-forge.example.com/your/repository/actions/runs/run_id",  # fill me in later
        email=getenv("PRIVATE_EMAIL"),
        name=getenv("PRIVATE_NAME"),
        repository_link="https://github.com/Tzahile/the-fork",
        resume_link="https://pdf-or-html-or-linkedin.example.com",  # fill me in later
        timestamp=get_iso8601(),
    )
    compact_payload = message.to_json().encode("utf-8")
    signature = ApiMessage.sign_hmac(compact_payload)

    request = Request(
        API_URL,
        compact_payload,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-Signature-256": "sha256=" + signature,
        },
    )

    # send data
    try:
        with urlopen(request, timeout=30) as response:
            res = response.read().decode("utf-8")  # I trust b12 response to be utf8
            print(json.loads(res)["receipt"])
            return 0
    except HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        print(f"HTTP error: {exc.code}", file=stderr)
        if error_body:
            print(error_body, file=stderr)
        return 1
    except URLError as exc:
        print(f"Request failed: {exc}", file=stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
