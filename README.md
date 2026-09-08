# Countdown Bot / 倒计时提醒 Bot

A GitHub Actions-based daily countdown reminder bot that sends one email per day through Gmail SMTP, with configurable target time and timezone.

一个基于 GitHub Actions 的每日倒计时提醒 Bot。GitHub Actions 每 5 分钟检查一次，脚本会读取 `config.json` 中设置的时区，并在该时区当地每天早上 09:00 之后的第一次检查时发送一封倒计时邮件；同一天只发送一次。

---

## 中文说明

### 这是什么？

这个项目不需要你自己维护服务器。

GitHub Actions 会每 5 分钟运行一次脚本。脚本会读取 `config.json` 中的时区，把当前时间转换成该时区的当地时间，并判断当地当天早上 09:00 是否已经到达。

如果已经到达 09:00，并且当天还没有发送过邮件，就会发送一次倒计时邮件。

```text
GitHub Actions
      ↓
每 5 分钟检查一次
      ↓
读取 config.json
      ↓
获取配置时区的当地时间
      ↓
判断当地当天早上 09:00 是否已到
      ↓
当天未发送过 → 发送邮件
      ↓
当天已发送过 → 跳过
```

当前默认目标时间：

```text
2030-01-01 00:00:00
```

当前默认时区：

```text
America/Los_Angeles
```

当前默认每日发送时间：

```text
当地早上 09:00
```

## 功能

- 使用 GitHub Actions 自动运行
- 每 5 分钟检查一次
- 根据 `config.json` 中的时区判断当地时间
- 每天当地早上 09:00 之后的第一次检查发送一次
- 同一天只发送一封倒计时邮件
- 通过 Gmail SMTP 发信
- 支持自定义目标日期和时间
- 支持 IANA 时区
- 自动处理夏令时
- 手机和电脑都可以通过邮箱收到提醒
- 使用状态文件避免同一天重复发送
- 手动运行 Workflow 时可立即发送测试邮件

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

改完以后，不需要再改 Workflow。

Bot 会自动按照纽约当地时间判断每天早上 09:00。

程序会自动处理夏令时，无需手动计算 UTC 时差。

### 修改每日发送小时

```json
"daily_push_hour": 9
```

`9` 表示该时区的当地早上 09:00。

Workflow 每 5 分钟检查一次，因此通常会在当地 09:00 之后的第一次检查时发送邮件。

GitHub Actions 的定时任务可能有调度延迟，所以无法保证邮件一定在 09:00:00 秒级送达。

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

不要填写普通 Gmail 登录密码。

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

## 邮件格式

邮件标题：

```text
距离2030还剩XXX天
```

邮件正文：

```text
剩余天数：XXXX 天

换算剩余小时数（去掉每天 7 小时睡觉时间）：XXXX 小时

当前时区：XXXX（要改手动在GitHub改）

你的时间 Token 不多了！
```

其中：

- `剩余天数` 会根据当前时间实时计算
- `换算剩余小时数` 按实际剩余总时间计算，并扣除每天 7 小时睡眠时间
- 当前算法相当于：`剩余总小时数 × 17 / 24`
- `当前时区` 直接读取 `config.json` 中的 `timezone`

## GitHub Actions 工作方式

Workflow 当前每 5 分钟运行一次：

```yaml
schedule:
  - cron: "*/5 * * * *"
```

Workflow 本身不写死任何时区。

每次运行后，Python 会：

1. 读取 `config.json` 中的 `timezone`
2. 获取该时区的当地时间
3. 读取 `daily_push_hour`
4. 判断当地当天早上 09:00 是否已经到达
5. 如果当天还没有发送邮件，则发送一次
6. 如果当天已经发送过，则跳过

因此以后更换所在地时，只需要修改：

```json
"timezone": "新的 IANA 时区"
```

不需要修改 Workflow。

## 手动测试

进入：

```text
Actions
→ Countdown Bot
→ Run workflow
```

手动运行 `Run workflow` 时，会跳过 09:00 时间限制，立即发送一封测试邮件。

正常的定时任务仍然遵守：

```text
配置时区的当地每天早上 09:00
```

## 安全与隐私

这个仓库可以保持 Public，但以下内容绝对不要直接写进公开文件：

```text
真实 Gmail 密码
Google App Password
其他 API Key / Token
```

这些都应该放在 GitHub Actions Secrets 中。

公开仓库里的 `config.json` 任何人都能看到，所以目标日期、标题和时区本身也属于公开信息。

普通访客可以看到公开仓库和 Actions 页面，但没有仓库写入权限的人不能手动触发 `Run workflow`。

---

# English

## What is this?

Countdown Bot is a lightweight daily countdown reminder powered by GitHub Actions.

GitHub Actions runs the script every 5 minutes. The Python script reads the timezone from `config.json`, converts the current time to that local timezone, and sends one email on the first check at or after local 09:00 each day.

```text
GitHub Actions
      ↓
Runs every 5 minutes
      ↓
Reads config.json
      ↓
Gets local time for the configured timezone
      ↓
Checks whether local 09:00 has been reached
      ↓
Not sent today → send email
      ↓
Already sent today → skip
```

Current default target:

```text
2030-01-01 00:00:00
```

Current default timezone:

```text
America/Los_Angeles
```

Current default daily send time:

```text
09:00 local time
```

## Features

- Automated with GitHub Actions
- Checks every 5 minutes
- Uses the timezone from `config.json`
- Sends once per day after local 09:00
- One countdown email per local day
- Gmail SMTP delivery
- Custom target date and time
- IANA timezone support
- Automatic daylight-saving-time handling
- Email delivery to phone and desktop
- Persistent state to prevent duplicate daily emails
- Manual workflow runs can send an immediate test email

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

After changing this value, no workflow edit is required.

The bot will automatically interpret the daily send time as 09:00 in the new timezone.

Daylight saving time is handled automatically.

### Change the daily send hour

```json
"daily_push_hour": 9
```

`9` means local 09:00 in the configured timezone.

Because the workflow checks every 5 minutes, the email is normally sent on the first check after local 09:00.

GitHub Actions schedules may be delayed, so second-level delivery at exactly 09:00:00 is not guaranteed.

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

## Email format

Subject:

```text
距离2030还剩XXX天
```

Body:

```text
剩余天数：XXXX 天

换算剩余小时数（去掉每天 7 小时睡觉时间）：XXXX 小时

当前时区：XXXX（要改手动在GitHub改）

你的时间 Token 不多了！
```

The remaining awake hours are calculated from the actual remaining total time using approximately:

```text
remaining total hours × 17 / 24
```

This subtracts 7 hours of sleep per day.

## How GitHub Actions works

The workflow runs every 5 minutes:

```yaml
schedule:
  - cron: "*/5 * * * *"
```

The workflow itself does not hard-code a timezone.

On every run, Python:

1. Reads `timezone` from `config.json`
2. Gets the current local time in that timezone
3. Reads `daily_push_hour`
4. Checks whether local 09:00 has been reached
5. Sends one email if no email has been sent that local day
6. Skips if the daily email has already been sent

To change location, only update:

```json
"timezone": "your IANA timezone"
```

No workflow change is required.

## Manual testing

Open:

```text
Actions
→ Countdown Bot
→ Run workflow
```

A manual workflow run bypasses the 09:00 time gate and sends a test email immediately.

Scheduled runs still follow the configured timezone and local morning send time.

## Security and privacy

The repository can remain public, but never commit the following values directly into public files:

```text
Your real Gmail password
Google App Password
Other API keys or tokens
```

Store them in GitHub Actions Secrets instead.

Remember that `config.json` is public, so the target date, title, and timezone are publicly visible.

Public visitors can view the repository and Actions history, but users without repository write access cannot manually trigger `Run workflow`.
