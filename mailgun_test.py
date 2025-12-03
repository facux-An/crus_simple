import os
import requests

def send_simple_message():
    domain = os.getenv("MAILGUN_DOMAIN")
    api_key = os.getenv("MAILGUN_API_KEY")
    to_address = os.getenv("TEST_TO", "fandrada153@gmail.com")

    if not domain or not api_key:
        raise RuntimeError("Faltan MAILGUN_DOMAIN o MAILGUN_API_KEY en el entorno")

    resp = requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        data={
            "from": f"Mailgun Sandbox <postmaster@{domain}>",
            "to": to_address,
            "subject": "Hello desde Mailgun sandbox",
            "text": "Prueba de envío desde mailgun_test.py"
        }
    )
    return resp

if __name__ == "__main__":
    r = send_simple_message()
    print("STATUS:", r.status_code)
    print(r.text)