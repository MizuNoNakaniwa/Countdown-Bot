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

    seconds = int((target - now).total_seconds())
    days = seconds // 86400 if seconds >= 0 else -1

    state = load_state()
    reason = None
    updates = {}

    today = now.strftime("%Y-%m-%d")
    hour_key = now.strftime("%Y-%m-%d-%H")

    if seconds <= 0 and not state.get("target_reached"):
        reason = "目标时间已到"
        updates["target_reached"] = True

    if reason is None and now.hour == int(cfg.get("daily_push_hour", 9)):
        if state.get("last_daily_date") != today:
            reason = "每日固定提醒"
            updates["last_daily_date"] = today

    milestones = set(int(x) for x in cfg.get("critical_day_milestones", []))
    milestone_key = f"day_{days}"
    if reason is None and days in milestones and not state.get(milestone_key):
        reason = f"关键节点：剩余 {days} 天"
        updates[milestone_key] = True

    if reason is None and cfg.get("final_day_hourly", True) and 0 <= seconds <= 86400:
        if state.get("last_final_hour") != hour_key:
            reason = "最后24小时每小时提醒"
            updates["last_final_hour"] = hour_key

    if reason is None:
        print("No email needed.")
        return

    remaining = format_remaining(max(seconds, 0))
    subject = f"[倒计时] {cfg.get('title', '目标倒计时')} — {remaining}"
    body = (
        f"{cfg.get('title', '目标倒计时')}\n\n"
        f"剩余：{remaining}\n"
        f"目标：{target.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"时区：{cfg['timezone']}\n"
        f"触发：{reason}\n\n"
        f"当前：{now.strftime('%Y-%m-%d %H:%M:%S')}\n"
    )

    send_email(subject, body)
    state.update(updates)
    save_state(state)
    print("Email sent:", reason)


if __name__ == "__main__":
    main()
