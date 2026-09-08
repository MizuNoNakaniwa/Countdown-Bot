# Countdown Bot / 倒计时提醒 Bot

A GitHub Actions-based countdown reminder bot with email and other notification methods, manual timezone switching, and customizable milestone reminders.

一个基于 GitHub Actions 的倒计时提醒 Bot，支持通过 Email 或其他方式发送提醒、手动切换时区，以及自定义关键节点提醒。

---

## 中文说明

### 这是什么？

Countdown Bot 是一个不需要自己维护服务器的倒计时提醒工具。

GitHub Actions 会定时运行脚本，计算距离目标时间还剩多久，并在满足提醒条件时通过 Telegram 推送消息；Email 可以作为备用通知通道。

```text
GitHub Actions
      ↓
每小时运行一次
      ↓
读取 config.json
      ↓
计算目标倒计时
      ↓
判断是否达到提醒条件
      ↓
Telegram / Email
      ↓
手机 + 电脑
```

### 功能

- GitHub Actions 自动运行
- Telegram 推送
- Email 备用提醒
- 手机和电脑同步接收
- 自定义目标日期和时间
- IANA 时区支持
- 自动处理夏令时
- 每天固定时间提醒
- 自定义关键节点
- 最后 24 小时可每小时提醒
- 状态文件防止重复通知

## 配置

主要配置位于 `config.json`：

```json
{
  "title": "目标倒计时",
  "target_datetime": "2027-01-01T00:00:00",
  "timezone": "America/Los_Angeles",
  "daily_push_hour": 9,
  "critical_day_milestones": [365, 180, 100, 30, 7, 3, 1, 0],
  "final_day_hourly": true,
  "telegram_enabled": true,
  "email_enabled": false
}
```

### 修改目标时间

```json
"target_datetime": "2027-01-01T00:00:00"
```

这个时间会按照 `timezone` 中指定的时区解释。

### 修改时区

不要使用固定的 `UTC-7`、`UTC+8`。推荐使用 IANA 时区名称：

```text
洛杉矶  America/Los_Angeles
纽约    America/New_York
伦敦    Europe/London
东京    Asia/Tokyo
上海    Asia/Shanghai
香港    Asia/Hong_Kong
```

例如从洛杉矶切换到纽约：

```json
"timezone": "America/New_York"
```

程序会自动处理夏令时，无需手动计算时差。

### 每日提醒时间

```json
"daily_push_hour": 9
```

表示程序会在当地时间上午 9 点所在的那次小时检查中发送每日提醒。GitHub Actions 不是实时调度系统，因此实际运行时间可能存在一定延迟。

### 关键节点

```json
"critical_day_milestones": [365, 180, 100, 30, 7, 3, 1, 0]
```

可自由修改，例如：

```json
"critical_day_milestones": [1000, 500, 365, 300, 200, 100, 50, 30, 7, 3, 1, 0]
```

### 最后 24 小时每小时提醒

开启：

```json
"final_day_hourly": true
```

关闭：

```json
"final_day_hourly": false
```

## Telegram 设置

### 1. 创建 Telegram Bot

在 Telegram 搜索官方 `@BotFather`，发送：

```text
/newbot
```

按提示创建 Bot 并保存 Bot Token。然后打开新 Bot，发送：

```text
/start
```

### 2. 获取 Chat ID

给 Bot 发过消息后，使用 Telegram Bot API 的 `getUpdates` 获取 Chat ID。结果中会出现类似：

```json
"chat": {
  "id": 123456789
}
```

这个数字就是你的 Chat ID。

### 3. 添加 GitHub Secrets

进入：

```text
Settings
→ Secrets and variables
→ Actions
→ New repository secret
```

添加：

```text
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
```

不要把 Bot Token 或 Chat ID 直接写进公开代码。

## Email 备用提醒

默认关闭：

```json
"email_enabled": false
```

如果要开启：

```json
"email_enabled": true
```

然后在 GitHub Secrets 中添加：

```text
SMTP_USERNAME
SMTP_PASSWORD
EMAIL_TO
```

如果使用 Gmail：

- `SMTP_USERNAME`：发件 Gmail 地址
- `SMTP_PASSWORD`：Google App Password
- `EMAIL_TO`：收件邮箱

不要使用普通 Gmail 密码。

## 安全与隐私

本仓库可以公开，但敏感信息必须放在 GitHub Secrets 中。

公开仓库中不要出现：

```text
真实 Email 地址
Telegram Bot Token
Telegram Chat ID
Gmail 密码
Google App Password
其他 API Key
```

这些值都应该保存在：

```text
Settings → Secrets and variables → Actions
```

注意：公开仓库中的 `config.json` 任何人都能看到。如果目标日期、标题或时区本身属于隐私信息，请不要直接填写真实值。

## 默认提醒规则

1. 每天当地时间约上午 9 点提醒一次
2. 剩余 365 天提醒
3. 剩余 180 天提醒
4. 剩余 100 天提醒
5. 剩余 30 天提醒
6. 剩余 7 天提醒
7. 剩余 3 天提醒
8. 剩余 1 天提醒
9. 最后 24 小时每小时提醒
10. 到达目标时间时提醒一次

GitHub Actions 每小时执行一次：

```yaml
schedule:
  - cron: "7 * * * *"
```

当地时间和时区计算由 Python 完成，因此切换所在地时不需要修改 Cron。

## 手动测试

进入：

```text
Actions → Countdown Bot → Run workflow
```

如果当前没有达到任何提醒条件，Workflow 会正常结束，但不会发送消息。

---

# English

## What is this?

Countdown Bot is a lightweight countdown reminder system powered by GitHub Actions.

It does not require a dedicated server. GitHub Actions periodically runs a Python script, calculates the time remaining until a configured target, and sends a notification when a reminder condition is met.

Telegram is the primary notification channel, while email can be enabled as a backup.

```text
GitHub Actions
      ↓
Runs every hour
      ↓
Reads config.json
      ↓
Calculates remaining time
      ↓
Checks reminder conditions
      ↓
Telegram / Email
      ↓
Phone + Desktop
```

## Features

- Automated with GitHub Actions
- Telegram notifications
- Optional email fallback
- Cross-device delivery
- Custom target date and time
- IANA timezone support
- Automatic daylight-saving-time handling
- Daily scheduled reminders
- Custom milestone reminders
- Optional hourly reminders during the final 24 hours
- Persistent state to prevent duplicate notifications

## Configuration

The main configuration file is `config.json`:

```json
{
  "title": "目标倒计时",
  "target_datetime": "2027-01-01T00:00:00",
  "timezone": "America/Los_Angeles",
  "daily_push_hour": 9,
  "critical_day_milestones": [365, 180, 100, 30, 7, 3, 1, 0],
  "final_day_hourly": true,
  "telegram_enabled": true,
  "email_enabled": false
}
```

### Target date and time

```json
"target_datetime": "2027-01-01T00:00:00"
```

The value is interpreted in the timezone specified by `timezone`.

### Timezone switching

Use IANA timezone names instead of fixed UTC offsets.

```text
Los Angeles  America/Los_Angeles
New York     America/New_York
London       Europe/London
Tokyo        Asia/Tokyo
Shanghai     Asia/Shanghai
Hong Kong    Asia/Hong_Kong
```

Example:

```json
"timezone": "America/New_York"
```

Daylight saving time is handled automatically.

### Daily notification hour

```json
"daily_push_hour": 9
```

The bot sends its daily reminder during the hourly check that occurs in the local 9 AM hour. GitHub Actions schedules are not guaranteed to run at an exact second and may be delayed.

### Milestones

```json
"critical_day_milestones": [365, 180, 100, 30, 7, 3, 1, 0]
```

These values can be customized freely.

### Final 24 hours

Enable hourly reminders:

```json
"final_day_hourly": true
```

Disable them:

```json
"final_day_hourly": false
```

## Telegram setup

### 1. Create a bot

Open Telegram, find the official `@BotFather`, and send:

```text
/newbot
```

Follow the instructions and save the Bot Token. Then open your new bot and send:

```text
/start
```

### 2. Find your Chat ID

After messaging the bot, use Telegram Bot API `getUpdates`. Look for a result similar to:

```json
"chat": {
  "id": 123456789
}
```

The numeric value is your Chat ID.

### 3. Add GitHub Secrets

Open:

```text
Settings
→ Secrets and variables
→ Actions
→ New repository secret
```

Create:

```text
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
```

Never hard-code these values into the public repository.

## Optional email fallback

Email is disabled by default:

```json
"email_enabled": false
```

Enable it with:

```json
"email_enabled": true
```

Then add these GitHub Secrets:

```text
SMTP_USERNAME
SMTP_PASSWORD
EMAIL_TO
```

For Gmail:

- `SMTP_USERNAME`: sending Gmail address
- `SMTP_PASSWORD`: Google App Password
- `EMAIL_TO`: recipient email address

Do not use your normal Gmail password.

## Security and privacy

This repository can safely be public as long as secrets are never committed into the codebase.

Never store the following directly in public files:

```text
Real email addresses
Telegram Bot Token
Telegram Chat ID
Gmail password
Google App Password
API keys
```

Store them in GitHub Actions Secrets instead:

```text
Settings → Secrets and variables → Actions
```

Note that `config.json` is public. If your target date, title, or timezone is sensitive, do not place real private values there.

## Default notification logic

1. Once per day around local 9 AM
2. At 365 days remaining
3. At 180 days remaining
4. At 100 days remaining
5. At 30 days remaining
6. At 7 days remaining
7. At 3 days remaining
8. At 1 day remaining
9. Every hour during the final 24 hours
10. Once when the target time is reached

GitHub Actions runs once per hour:

```yaml
schedule:
  - cron: "7 * * * *"
```

Timezone calculations are handled in Python, so changing your location does not require changing the workflow schedule.

## Manual test

Open:

```text
Actions → Countdown Bot → Run workflow
```

If no reminder condition is currently active, the workflow will complete successfully without sending a notification.
