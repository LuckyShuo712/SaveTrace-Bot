# 🗂️「存迹」（SaveTrace-Bot）

<p align="center">
<img src="https://img.shields.io/badge/Python-3.10-blue?logo=python" />
<img src="https://img.shields.io/badge/Pyrogram-2.0-orange?logo=telegram" />
<img src="https://img.shields.io/badge/Docker-Supported-2496ED?logo=docker" />
<img src="https://img.shields.io/badge/Telegram-Bot-26A5E4?logo=telegram" />
</p>
<p align="center">
<b>一个Telegram Bot，用于保存 Telegram 中的限制转发内容。</b>
<br>
支持公开频道、私有频道、机器人消息、媒体文件获取。<br>
基于 <a href="https://github.com/bipinkrish/Save-Restricted-Bot">Save-Restricted-Bot</a> 二次开发</p>

---

# ✨ 项目介绍

**「存迹」（SaveTrace-Bot）** 是一个基于 **Python + Pyrogram** 开发的 Telegram 内容处理机器人。
它可以帮助用户通过 Telegram 消息链接获取内容，并自动转发到当前聊天。
支持：
* 🌍 公开频道内容获取（直接转发原消息）
* 🔒 私有频道内容获取（先下载后上传至Bot）
* 🤖 Bot Chat 消息获取
* 🖼 图片保存
* 🎬 视频保存
* 📁 文件保存
* 🎵 音频保存
* 🎞 动图保存
* 📦 Telegram 相册完整转发
* 👥 用户授权管理
* 🐳 Docker Compose 部署
---
# 📸 功能展示
## 🚀 简单使用
发送 Telegram 消息链接：
```
https://t.me/channel/1234
```
机器人自动获取对应内容。

---

## 📦 Telegram 相册支持

支持完整获取：

```
🖼 图片1
🖼 图片2
🖼 图片3
🖼 图片4
```

不会只发送第一张图片。

---

# 🛠️ 技术架构

| 组件                | 说明              |
| ----------------- | --------------- |
| 🐍 Python         | 核心开发语言          |
| 📡 Pyrogram       | Telegram API 框架 |
| 🐳 Docker         | 容器化运行           |
| ⚙️ Docker Compose | 自动部署管理          |

---

# 📋 使用方法

## 🌍 公开频道

直接发送：

```
https://t.me/channel/message_id
```

示例：

```
https://t.me/example/100
```

机器人会自动发送消息内容。

---

## 🔒 私有频道

首先发送邀请链接：

```
https://t.me/+xxxxxxxx
```

然后发送：

```
https://t.me/c/channel_id/message_id
```

> 如果绑定账号已经加入频道，可以跳过邀请链接。

---

## 🤖 Bot 消息

格式：

```
https://t.me/b/botusername/message_id
```

示例：

```
https://t.me/b/examplebot/4321
```

---

## 📦 批量获取

格式：

```
开始ID-结束ID
```

示例：

```
https://t.me/example/100-120
```

机器人会依次获取：

```
100
101
102
...
120
```

---

# 🐳 Docker 部署

## 1️⃣ 下载项目

```bash
git clone https://github.com/LuckyShuo712/SaveTrace-Bot.git

cd SaveTrace-Bot
```

---

## 2️⃣ 配置文件

编辑：

```bash
nano config.json
```

填写：

```json
{
    "TOKEN": "你的Bot Token",
    "ID": "Telegram API ID",
    "HASH": "Telegram API HASH",
    "STRING": "String Session",
    "OWNER": 123456789,
    "USERS": [
        123456789,
        987654321
    ]
}
```

---

## 3️⃣ 启动 Bot

```bash
docker compose up -d
```

查看运行状态：

```bash
docker compose ps
```

查看日志：

```bash
docker compose logs -f
```

---

# ⚙️ 管理命令

| 命令          | 功能     |
| ----------- | ------ |
| `/start`    | 启动机器人  |
| `/help`     | 查看使用教程 |
| `/add 用户ID` | 添加授权用户 |
| `/del 用户ID` | 删除授权用户 |
| `/users`    | 查看授权列表 |

---

# 🔐 权限系统

「存迹」支持用户授权机制：

* 👑 管理员永久拥有权限
* 👥 普通用户需要授权
* 🚫 未授权用户无法使用

---

# ⚠️ 注意事项

## Telegram API

需要申请：

* API ID
* API HASH

申请地址：

```
https://my.telegram.org
```

---

# 🌟 开源协议

本项目仅供学习与研究使用。

使用过程中请遵守：

* Telegram 服务条款
* 当地法律法规
* 内容版权规定

---

# ❤️ 支持项目

如果这个项目帮助到了你：

⭐ Star 项目

🐛 提交 Issue

💡 提交改进建议

---

<p align="center">

Made with ❤️ by LuckyShuo

</p>
