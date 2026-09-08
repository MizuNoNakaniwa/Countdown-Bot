import json
import os
import smtplib
from datetime import datetime
from email.message import EmailMessage
from zoneinfo import ZoneInfo

STATE_FILE = ".countdown_state.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_state():
    try:
        return load_json(STATE_FILE)
    except Exception:
        return {}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def send_email(subject, body):
    host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    port = int(os.getenv("SMTP_PORT", "465"))
    user = os.environ["SMTP_USERNAME"]
    password = os.environ["SMTP_PASSWORD"]
    recipient = os.environ["EMAIL_TO"]

    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL(host, port, timeout=30) as smtp:
        smtp.login(user, password)
        smtp.send_message(msg)


def main():
    cfg = load_json("config.json")
    tz = ZoneInfo(cfg["timezone"])
    now = datetime.now(tz)
    target = datetime.fromisoformat(cfg["target_datetime"]).replace(tzinfo=tz)

    manual_test = os.getenv("GITHUB_EVENT_NAME") == "workflow_dispatch"
    state = load_state()
    today = now.strftime("%Y-%m-%d")

    if not manual_test:
        if now.hour != int(cfg.get("daily_push_hour", 9)):
            print("Not the configured local send hour.")
            return

        if state.get("last_daily_date") == today:
            print("Today's email has already been sent.")
            return

    seconds = max(int((target - now).total_seconds()), 0)
    remaining_days = seconds // 86400
    remaining_awake_hours = int((seconds / 3600) * (17 / 24))

    subject = f"距离2030还剩{remaining_days}天"
    body = (
        f"剩余天数：{remaining_days} 天\n\n"
        f"换算剩余小时数（去掉每天 7 小时睡觉时间）：{remaining_awake_hours} 小时\n\n"
        f"当前时区：{cfg['timezone']}（要改手动在GitHub改）\n\n"
        f"你的时间 Token 不多了！\n"
    )

    send_email(subject, body)

    if manual_test:
        print("Test countdown email sent.")
    else:
        state["last_daily_date"] = today
        save_state(state)
        print("Daily countdown email sent.")


if __name__ == "__main__":
    main()
