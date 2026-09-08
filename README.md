# Countdown Bot / 倒计时提醒 Bot

A GitHub Actions-based daily countdown reminder bot that sends one email per day through Gmail SMTP, with configurable target time and timezone.

一个基于 GitHub Actions 的每日倒计时提醒 Bot。GitHub Actions 负责定时运行，脚本每天通过 Gmail SMTP 向指定邮箱发送一次当前倒计时，并支持自定义目标时间与时区。

---

## 中文说明

### 这是什么？

这个项目不需要你自己维护服务器。

GitHub Actions 会每小时运行一次脚本，但脚本只会在你设置的当地时间那一个小时内发送邮件，而且同一天只发送一次。

```text
GitHub Actions
      ↓
每小时检查一次
      ↓
读取 config.json
      ↓
判断是否到了每日发送时间
      ↓
计算距离目标时间还剩多久
      ↓
通过 Gmail SMTP 发邮件
      ↓
你的收件邮箱
```

当前默认目标时间是：

```text
2030-01-01 00:00:00
```

当前默认时区是：

```text
America/Los_Angeles
```

当前默认每日发送时间是当地时间：

```text
09:00
```

## 功能

- 使用 GitHub Actions 自动运行
- 每天只发送一封倒计时邮件
- 通过 Gmail SMTP 发信
- 支持自定义目标日期和时间
- 支持 IANA 时区
- 自动处理夏令时
- 手机和电脑都可以通过邮箱收到提醒
- 使用状态文件避免同一天重复发送

## 当前配置

`config.json`：

```json
{
  "title": "目标倒计时",
  "target_datetime": "2030-01-01T00:00:00",
  "timezone": "America/Los_Angeles",
  "daily_push_hour": 9
}
```

### 修改目标时间

例如：

```json
"target_datetime": "2030-01-01T00:00:00"
```

这个时间会按照 `timezone` 指定的当地时区解释。

### 修改时区

推荐使用 IANA 时区名称：

```text
洛杉矶  America/Los_Angeles
纽约    America/New_York
伦敦    Europe/London
东京    Asia/Tokyo
上海    Asia/Shanghai
香港    Asia/Hong_Kong
```

例如：

```json
"timezone": "America/New_York"
```

无需自己计算 UTC 时差，夏令时会自动处理。

### 修改每日发送时间

```json
"daily_push_hour": 9
```

表示在所选时区的当地时间 9 点所在的那一个小时内发送一次。

GitHub Actions 不是精确到秒的定时器，所以实际执行可能会有一定延迟。

## Gmail / Email 设置

进入仓库：

```text
Settings
→ Secrets and variables
→ Actions
→ New repository secret
```

创建以下 3 个 Repository Secrets：

```text
SMTP_USERNAME
SMTP_PASSWORD
EMAIL_TO
```

### SMTP_USERNAME

填写用于发信的 Gmail 地址，例如：

```text
example@gmail.com
```

### SMTP_PASSWORD

填写 Google App Password，也就是 Google 的应用专用密码。

不要填写你的普通 Gmail 登录密码。

通常需要先开启 Google 两步验证，然后创建一个 App Password。

### EMAIL_TO

填写真正接收倒计时邮件的邮箱。

它可以和 `SMTP_USERNAME` 是同一个邮箱，也可以是另一个邮箱。

例如：

```text
SMTP_USERNAME = example@gmail.com
SMTP_PASSWORD = 你的 16 位 Google App Password
EMAIL_TO      = example@gmail.com
```

这表示由这个 Gmail 账号给自己发送每日倒计时邮件。

## 邮件内容

每天收到的邮件大致会包含：

```text
目标倒计时

剩余：xxxx 天 xx:xx:xx
目标：2030-01-01 00:00:00
时区：America/Los_Angeles
当前：当前当地时间
```

邮件标题中也会直接显示当前剩余时间。

## GitHub Actions 工作方式

Workflow 当前每小时运行一次：

```yaml
schedule:
  - cron: "7 * * * *"
```

Cron 使用 UTC，但你不需要根据所在地手动修改它。

脚本会读取 `config.json` 中的 `timezone`，自己判断当前当地时间是否已经进入 `daily_push_hour`。

所以切换地点时，只需要改 `timezone`。

## 手动测试

进入：

```text
Actions
→ Countdown Bot
→ Run workflow
```

注意：当前脚本即使手动运行，也只会在配置的 `daily_push_hour` 那个当地小时内真正发信。

如果需要立即测试，可以暂时把：

```json
"daily_push_hour": 9
```

改成你当前所在地的当前小时，然后手动运行一次 Workflow。

测试完成后再改回你想要的每日提醒时间。

## 安全与隐私

这个仓库可以保持 Public，但以下内容绝对不要直接写进公开文件：

```text
真实 Gmail 密码
Google App Password
其他 API Key / Token
```

这些都应该放在 GitHub Actions Secrets 中。

公开仓库里的 `config.json` 任何人都能看到，所以目标日期、标题和时区本身也属于公开信息。

---

# English

## What is this?

Countdown Bot is a lightweight daily countdown reminder powered by GitHub Actions.

GitHub Actions runs the script every hour, but the script sends at most one email per local day and only during the configured local send hour.

```text
GitHub Actions
      ↓
Runs every hour
      ↓
Reads config.json
      ↓
Checks the configured local send hour
      ↓
Calculates remaining time
      ↓
Sends email through Gmail SMTP
      ↓
Your inbox
```

The current default target is:

```text
2030-01-01 00:00:00
```

Default timezone:

```text
America/Los_Angeles
```

Default daily send hour:

```text
09:00 local time
```

## Features

- Automated with GitHub Actions
- One countdown email per day
- Gmail SMTP delivery
- Custom target date and time
- IANA timezone support
- Automatic daylight-saving-time handling
- Email delivery to phone and desktop
- Persistent state to prevent duplicate daily emails

## Current configuration

`config.json`:

```json
{
  "title": "目标倒计时",
  "target_datetime": "2030-01-01T00:00:00",
  "timezone": "America/Los_Angeles",
  "daily_push_hour": 9
}
```

### Change the target time

```json
"target_datetime": "2030-01-01T00:00:00"
```

The target is interpreted in the timezone specified by `timezone`.

### Change the timezone

Use IANA timezone names:

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

You do not need to manually calculate UTC offsets. Daylight saving time is handled automatically.

### Change the daily send hour

```json
"daily_push_hour": 9
```

This means the bot sends during the local 9 AM hour in the configured timezone.

GitHub Actions scheduling is not guaranteed to run at an exact second, so some delay is possible.

## Gmail / Email setup

Open the repository and go to:

```text
Settings
→ Secrets and variables
→ Actions
→ New repository secret
```

Create these three Repository Secrets:

```text
SMTP_USERNAME
SMTP_PASSWORD
EMAIL_TO
```

### SMTP_USERNAME

The Gmail account used to send the message.

Example:

```text
example@gmail.com
```

### SMTP_PASSWORD

A Google App Password.

Do not use your normal Gmail password.

You generally need to enable Google 2-Step Verification first, then create an App Password.

### EMAIL_TO

The email address that receives the countdown message.

It may be the same address as `SMTP_USERNAME` or a different address.

Example:

```text
SMTP_USERNAME = example@gmail.com
SMTP_PASSWORD = your 16-character Google App Password
EMAIL_TO      = example@gmail.com
```

This configuration makes the Gmail account send the daily countdown email to itself.

## Email content

A daily message will look roughly like this:

```text
目标倒计时

剩余：xxxx 天 xx:xx:xx
目标：2030-01-01 00:00:00
时区：America/Los_Angeles
当前：current local time
```

The remaining time is also included in the email subject.

## How GitHub Actions works

The workflow currently runs once per hour:

```yaml
schedule:
  - cron: "7 * * * *"
```

The cron schedule uses UTC, but you do not need to adjust it when moving between locations.

The Python script reads the IANA timezone from `config.json` and decides whether the current run falls within the configured local send hour.

To change location, only update `timezone`.

## Manual testing

Open:

```text
Actions
→ Countdown Bot
→ Run workflow
```

The current implementation still respects `daily_push_hour` during a manual run.

For an immediate test, temporarily change `daily_push_hour` to the current hour in your configured timezone, run the workflow manually, then change it back afterward.

## Security and privacy

The repository can remain public, but never commit the following values directly into public files:

```text
Your real Gmail password
Google App Password
Other API keys or tokens
```

Store them in GitHub Actions Secrets instead.

Remember that `config.json` is public, so the target date, title, and timezone are also publicly visible.
