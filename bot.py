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


def format_remaining(seconds):
    if seconds <= 0:
        return "已到达目标时间"
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, secs = divmod(rem, 60)
    return f"{days} 天 {hours:02d}:{minutes:02d}:{secs:02d}"


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

    # The workflow checks hourly, but the bot sends at most one email per local day.
    if now.hour != int(cfg.get("daily_push_hour", 9)):
        print("Not the configured local send hour.")
        return

    state = load_state()
    today = now.strftime("%Y-%m-%d")
    if state.get("last_daily_date") == today:
        print("Today's email has already been sent.")
        return

    seconds = int((target - now).total_seconds())
    remaining = format_remaining(max(seconds, 0))
    title = cfg.get("title", "目标倒计时")

    subject = f"[倒计时] {title} — {remaining}"
    body = (
        f"{title}\n\n"
        f"剩余：{remaining}\n"
        f"目标：{target.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"时区：{cfg['timezone']}\n"
        f"当前：{now.strftime('%Y-%m-%d %H:%M:%S')}\n"
    )

    send_email(subject, body)
    state["last_daily_date"] = today
    save_state(state)
    print("Daily countdown email sent.")


if __name__ == "__main__":
    main()
