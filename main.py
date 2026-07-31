import json
import os
import threading
import time

import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import (
    InviteHashExpired,
    UserAlreadyParticipant,
    UsernameNotOccupied,
)
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


# ==========================
# Config
# ==========================

with open("config.json", "r", encoding="utf-8") as f:
    DATA = json.load(f)

def getenv(name):
    return os.environ.get(name) or DATA.get(name)
# ==========================
# Permission System
# ==========================

OWNER = DATA.get("OWNER")
ALLOWED_USERS = DATA.get(
    "USERS",
    []
)

def save_config():
    with open(
        "config.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            DATA,
            f,
            indent=4,
            ensure_ascii=False
        )

def notify_owner(text, keyboard=None):
    bot.send_message(
        OWNER,
        text,
        reply_markup=keyboard
    )

def is_allowed(message):
    if not message.from_user:
        return False
    user_id = message.from_user.id
    return (
        user_id == OWNER
        or
        user_id in ALLOWED_USERS
    )
def is_owner(message):
    if not message.from_user:
        return False
    return (
        message.from_user.id
        ==
        OWNER
    )

API_ID = getenv("ID")
API_HASH = getenv("HASH")
BOT_TOKEN = getenv("TOKEN")
STRING_SESSION = getenv("STRING")

bot = Client(
    "mybot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

if STRING_SESSION:

    acc = Client(
        "myacc",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=STRING_SESSION,
    )

    acc.start()
else:
    acc = None


# ==========================
# Download / Upload Status
# ==========================


def downstatus(status_file, message):
    while not os.path.exists(status_file):
        time.sleep(1)
    time.sleep(3)
    while os.path.exists(status_file):
        try:
            with open(status_file, "r") as f:
                progress_text = f.read()

            bot.edit_message_text(
                message.chat.id,
                message.id,
                f"📥 **下载进度：** `{progress_text}`",
            )
            time.sleep(10)
        except Exception:
            time.sleep(5)

def upstatus(status_file, message):

    while not os.path.exists(status_file):
        time.sleep(1)
    time.sleep(3)
    while os.path.exists(status_file):
        try:
            with open(status_file, "r") as f:
                progress_text = f.read()
            bot.edit_message_text(
                message.chat.id,
                message.id,
                f"📤 **上传进度：** `{progress_text}`",
            )
            time.sleep(10)
        except Exception:
            time.sleep(5)

def progress(current, total, message, status_type):
    with open(
        f"{message.id}{status_type}status.txt",
        "w",
    ) as f:
        f.write(
            f"{current * 100 / total:.1f}%"
        )


# ==========================
# Start Command
# ==========================


@bot.on_message(filters.command(["start"]))
def send_start(client, message):
    if not is_allowed(message):
        bot.send_message(
            message.chat.id,
            """
⛔ **暂无使用权限**

点击下面按钮申请使用权限。
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "📩 申请使用",
                            callback_data=f"apply_{message.from_user.id}"
                        )
                    ]
                ]
            ),

            reply_to_message_id=message.id
        )

        return
        
    bot.send_message(
        message.chat.id,
        f"""
👋 **你好 {message.from_user.mention}**
🤖 **欢迎使用「存迹」**
📥 我可以帮助你获取 Telegram
无法直接保存的受限内容。
━━━━━━━━━━━━━━
✨ **支持内容**
🖼 图片
🎬 视频
📁 文件
🎵 音频
🎞 动图
📦 多媒体消息
━━━━━━━━━━━━━━
🚀 **使用方法**
直接发送 Telegram 帖子链接即可。
📚 输入 /help 查看教程
❤️ 感谢你的使用
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💻 「存迹」代码",
                        url=(
                            "https://github.com/"
                            "fzucs/"
                            "Save-Restricted-Bot"
                        ),
                    )
                ]
            ]
        ),
        reply_to_message_id=message.id,
    )


# ==========================
# Private Album Handler
# ==========================

def get_private_album(chat_id, message):

    """
    获取 Telegram Media Group
    """

    if not message.media_group_id:
        return [message]
    album = []


    # Telegram 相册消息通常连续
    # 搜索范围扩大到前后50条

    for msg_id in range(
        message.id - 50,
        message.id + 50,
    ):

        try:

            msg = acc.get_messages(
                chat_id,
                msg_id,
            )

            if (
                msg
                and
                msg.media_group_id
                ==
                message.media_group_id
            ):

                album.append(msg)
        except Exception:
            pass

    album.sort(
        key=lambda x: x.id
    )

    return album


# ==========================
# Send Private Album
# ==========================


def send_private_album(
    message,
    album,
):

    from pyrogram.types import (
        InputMediaDocument,
        InputMediaPhoto,
        InputMediaVideo,
    )

    media = []
    files = []
    for msg in album:
        try:
            file = acc.download_media(
                msg
            )

            if not file:
                continue
            files.append(file)
            caption = None


            # Telegram Album
            # 通常只有第一条有文字

            if msg.caption:
                caption = msg.caption

            if msg.photo:
                media.append(
                    InputMediaPhoto(
                        file,
                        caption=caption,
                        caption_entities=(
                            msg.caption_entities
                        ),
                    )
                )

            elif msg.video:
                media.append(
                    InputMediaVideo(
                        file,
                        caption=caption,
                        caption_entities=(
                            msg.caption_entities
                        ),
                    )
                )

            elif msg.document:
                media.append(
                    InputMediaDocument(
                        file,
                        caption=caption,
                        caption_entities=(
                            msg.caption_entities
                        ),
                    )
                )

        except Exception as e:
            print(
                "Album download error:",
                e,
            )

    if not media:
        return

    # Telegram限制一次最多10个媒体

    for index in range(
        0,
        len(media),
        10,
    ):

        bot.send_media_group(
            chat_id=message.chat.id,
            media=media[index:index + 10],
            reply_to_message_id=message.id,

        )

    # 删除缓存文件

    for file in files:
        try:
            if os.path.exists(file):
                os.remove(file)
        except Exception:
            pass



# ==========================
# Handle Private Message
# ==========================


def handle_private(
    message,
    chat_id,
    msg_id,
):

    try:
        msg = acc.get_messages(
            chat_id,
            msg_id,
        )

        if not msg:
            bot.send_message(
                message.chat.id,
                "❌ **消息不存在**",
                reply_to_message_id=message.id,
            )

            return


        # ======================
        # Album
        # ======================


        album = get_private_album(
            chat_id,
            msg,
        )

        if len(album) > 1:

            status = bot.send_message(
                message.chat.id,
                "📥 **正在下载相册...**\n\n"
                "⏳ 请稍候",
                reply_to_message_id=message.id,
            )

            send_private_album(
                message,
                album,
            )

            bot.delete_messages(
                message.chat.id,
                status.id,
            )

            return


        # ======================
        # Single Message
        # ======================


        msg_type = get_message_type(
            msg
        )

        if msg_type == "Text":

            bot.send_message(
                message.chat.id,
                msg.text,
                entities=msg.entities,
                reply_to_message_id=message.id,
            )

            return

        status = bot.send_message(
            message.chat.id,
            "📥 **正在下载文件...**",
            reply_to_message_id=message.id,
        )

        download_file = acc.download_media(
            msg,
            progress=progress,
            progress_args=[
                message,
                "down",
            ],
        )

        if msg_type == "Photo":

            bot.send_photo(
                message.chat.id,
                download_file,
                caption=msg.caption,
                caption_entities=msg.caption_entities,
                reply_to_message_id=message.id,
            )

        elif msg_type == "Video":

            bot.send_video(
                message.chat.id,
                download_file,
                duration=msg.video.duration,
                width=msg.video.width,
                height=msg.video.height,
                caption=msg.caption,
                caption_entities=msg.caption_entities,
                reply_to_message_id=message.id,
            )

        elif msg_type == "Document":

            bot.send_document(
                message.chat.id,
                download_file,
                caption=msg.caption,
                caption_entities=msg.caption_entities,
                reply_to_message_id=message.id,
            )

        elif msg_type == "Audio":

            bot.send_audio(
                message.chat.id,
                download_file,
                caption=msg.caption,
                caption_entities=msg.caption_entities,
                reply_to_message_id=message.id,
            )

        elif msg_type == "Animation":

            bot.send_animation(
                message.chat.id,
                download_file,
                reply_to_message_id=message.id,
            )

        elif msg_type == "Sticker":

            bot.send_sticker(
                message.chat.id,
                download_file,
                reply_to_message_id=message.id,
            )

        elif msg_type == "Voice":

            bot.send_voice(
                message.chat.id,
                download_file,
                caption=msg.caption,
                reply_to_message_id=message.id,
            )

        bot.delete_messages(
            message.chat.id,
            status.id,
        )

        if os.path.exists(download_file):

            os.remove(download_file)

    except Exception as e:

        bot.send_message(
            message.chat.id,
            f"""
❌ **处理失败**

错误：

`{e}`
""",
            reply_to_message_id=message.id,
        )

# ==========================
# Detect Message Type
# ==========================


def get_message_type(message):

    try:
        message.document.file_id
        return "Document"
    except Exception:
        pass

    try:
        message.video.file_id
        return "Video"
    except Exception:
        pass


    try:
        message.animation.file_id
        return "Animation"
    except Exception:
        pass

    try:
        message.sticker.file_id
        return "Sticker"
    except Exception:
        pass

    try:
        message.voice.file_id
        return "Voice"
    except Exception:
        pass

    try:
        message.audio.file_id
        return "Audio"
    except Exception:
        pass

    try:
        message.photo.file_id
        return "Photo"
    except Exception:
        pass

    try:
        message.text
        return "Text"
    except Exception:
        return None


# ==========================
# Usage Text
# ==========================


USAGE = """
📚 **「存迹」使用教程**
━━━━━━━━━━━━━━
🌍 **公开频道**
直接发送帖子链接：
```
https://t.me/xxxx/1234
```
机器人会自动发送内容。
━━━━━━━━━━━━━━
🔒 **私有频道**
步骤：
① 发送频道邀请链接
例如：
```
https://t.me/+xxxxxxxx
```
② 再发送帖子链接
如果账号已经加入频道，第一步可以跳过。
━━━━━━━━━━━━━━
🤖 **机器人消息**
格式：
```
https://t.me/b/botusername/message_id
```
示例：
```
https://t.me/b/examplebot/4321
```
━━━━━━━━━━━━━━
📦 **批量获取**
格式：
```
开始ID-结束ID
https://t.me/channel/100-120
```
私有频道：
```
https://t.me/c/123456/100-120
```
━━━━━━━━━━━━━━
💡 支持：
🖼 图片
🎬 视频
📁 文件
🎵 音频
🎞 动图
📦 Telegram 相册
━━━━━━━━━━━━━━
🚀 发送链接开始使用！
"""

# ==========================
# Add User
# ==========================

@bot.on_message(filters.command("add"))
def add_user(client, message):
    if not is_owner(message):
        return
    try:
        user_id = int(
            message.text.split()[1]
        )
    except:
        bot.send_message(
            message.chat.id,
            "格式：\n/add 用户ID"
        )
        return
    if user_id not in ALLOWED_USERS:
        ALLOWED_USERS.append(
            user_id
        )
    DATA["USERS"] = ALLOWED_USERS
    save_config()
    bot.send_message(
        message.chat.id,
        f"✅ 添加成功\n\n用户ID:\n`{user_id}`"
    )

# ==========================
# Delete User
# ==========================

@bot.on_message(filters.command("del"))
def del_user(client, message):
    if not is_owner(message):
        return
    try:
        user_id = int(
            message.text.split()[1]
        )
    except:
        bot.send_message(
            message.chat.id,
            "格式：\n/del 用户ID"
        )
        return
    if user_id in ALLOWED_USERS:
        ALLOWED_USERS.remove(
            user_id
        )
    DATA["USERS"] = ALLOWED_USERS
    save_config()
    bot.send_message(
        message.chat.id,
        f"✅ 删除成功\n\n用户ID:\n`{user_id}`"
    )

# ==========================
# List Users
# ==========================

@bot.on_message(filters.command("users"))
def list_users(client, message):
    print("users command loaded")
    if not is_owner(message):
        return
    text = "👥 授权用户：\n\n"
    for user in ALLOWED_USERS:
        text += (
            f"`{user}`\n"
        )
    bot.send_message(
        message.chat.id,
        text
    )

# ==========================
# Help Command
# ==========================


@bot.on_message(filters.command("help"))
def help_command(client, message):
    if not is_allowed(message):
        return

    bot.send_message(
        message.chat.id,
        USAGE,
        reply_to_message_id=message.id
    )


# ==========================
# About Command
# ==========================


@bot.on_message(filters.command("about"))
def about_command(client, message):

    bot.send_message(
        message.chat.id,
        """
🤖 **「存迹」**
━━━━━━━━━━━━━━
📌 功能：
• 获取 Telegram 受限内容
• 支持公开频道
• 支持私有频道
• 支持图片相册
• 支持视频相册
• 支持文件下载
━━━━━━━━━━━━━━
⚙️ Powered by Luckyshuo
💻 「存迹」项目

""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🌐 「存迹」",
                        url=(
                            "https://github.com/"
                            "fzucs/"
                            "Save-Restricted-Bot"
                        ),
                    )
                ]
            ]
        ),
        reply_to_message_id=message.id,
    )

from pyrogram import enums
@bot.on_callback_query()
def callback_handler(client, callback_query):
    data = callback_query.data
    if data.startswith(
        "apply_"
    ):
        user_id = int(
            data.split("_")[1]
        )
        user = callback_query.from_user
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✅ 同意",
                        callback_data=f"approve_{user_id}"
                    ),

                    InlineKeyboardButton(
                        "❌ 拒绝",
                        callback_data=f"reject_{user_id}"
                    )
                ]
            ]
        )

        bot.send_message(
            OWNER,
            f"""
📢 **用户申请授权**
👤 名称：
{user.first_name}
🆔 ID：
`{user.id}`
🔗 用户名：
@{user.username}
""",
            reply_markup=keyboard
        )
        callback_query.answer(
            "申请已发送"
        )
        bot.edit_message_text(
            callback_query.message.chat.id,
            callback_query.message.id,
            """
✅ 申请已经提交
请等待管理员审核。
"""
        )
@bot.on_callback_query()
def approve_handler(client, callback_query):
    data = callback_query.data
    # 同意
    
    if data.startswith(
        "approve_"
    ):
        if callback_query.from_user.id != OWNER:
            callback_query.answer(
                "没有权限"
            )
            return
        user_id = int(
            data.split("_")[1]
        )
        if user_id not in ALLOWED_USERS:
            ALLOWED_USERS.append(
                user_id
            )
        DATA["USERS"] = ALLOWED_USERS
        save_config()
        bot.send_message(
            user_id,
            """
🎉 **授权成功**
你现在可以使用机器人。
"""
        )
        callback_query.message.edit_text(
            "✅ 已授权用户\n\n"
            f"ID: `{user_id}`"
        )
        
    # 拒绝
    elif data.startswith(
        "reject_"
    ):
        if callback_query.from_user.id != OWNER:
            return
        user_id = int(
            data.split("_")[1]
        )
        bot.send_message(
            user_id,
            """
❌ 授权申请被拒绝。
"""
        )
        callback_query.message.edit_text(
            "❌ 已拒绝申请"
        )

# ==========================
# Message Handler
# ==========================

@bot.on_message(
    filters.text &
    ~filters.regex(r"^/")
)
def save_message(client, message):
    if not is_allowed(message):

        bot.send_message(
            message.chat.id,
            "⛔ 你没有使用权限",
            reply_to_message_id=message.id
        )

        return
    text = message.text
    print(text)
    
    # ======================
    # Join Private Chat
    # ======================

    if (
        "https://t.me/+" in text
        or
        "https://t.me/joinchat/" in text
    ):
        if acc is None:
            bot.send_message(
                message.chat.id,
                "⚠️ **未配置 String Session**",
                reply_to_message_id=message.id,
            )
            return
        try:
            acc.join_chat(text)
            bot.send_message(
                message.chat.id,
                "✅ **已成功加入频道/群组**",
                reply_to_message_id=message.id,
            )
        except UserAlreadyParticipant:
            bot.send_message(
                message.chat.id,
                "ℹ️ **已经加入该频道/群组**",
                reply_to_message_id=message.id,
            )
        except InviteHashExpired:
            bot.send_message(
                message.chat.id,
                "❌ **邀请链接无效或已过期**",
                reply_to_message_id=message.id,
            )
        except Exception as e:
            bot.send_message(
                message.chat.id,
                f"❌ **加入失败**\n\n`{e}`",
                reply_to_message_id=message.id,
            )
        return


    # ======================
    # Telegram Post Link
    # ======================

    if "https://t.me/" not in text:
        return
    try:
        parts = text.split("/")
        ids = (
            parts[-1]
            .replace("?single", "")
            .split("-")
        )
        start_id = int(ids[0].strip())
        try:
            end_id = int(
                ids[1].strip()
            )
        except Exception:
            end_id = start_id

    except Exception:

        bot.send_message(
            message.chat.id,
            "❌ **链接格式错误**",
            reply_to_message_id=message.id,
        )
        return
    for msg_id in range(
        start_id,
        end_id + 1,
    ):


        # ==================
        # Private Channel
        # ==================

        if "https://t.me/c/" in text:
            try:
                chat_id = int(
                    "-100" + parts[4]
                )
            except Exception:
                bot.send_message(
                    message.chat.id,
                    "❌ **私有频道链接错误**",
                    reply_to_message_id=message.id,
                )

                return

            if acc is None:

                bot.send_message(
                    message.chat.id,
                    "⚠️ **未配置 String Session**",
                    reply_to_message_id=message.id,
                )

                return

            handle_private(
                message,
                chat_id,
                msg_id,
            )


        # ==================
        # Bot Chat
        # ==================

        elif "https://t.me/b/" in text:
            username = parts[4]

            if acc is None:

                bot.send_message(
                    message.chat.id,
                    "⚠️ **未配置 String Session**",
                    reply_to_message_id=message.id,
                )

                return

            handle_private(
                message,
                username,
                msg_id,
            )



        # ==================
        # Public Channel
        # ==================

        else:
            username = parts[3]
            try:
                msg = bot.get_messages(
                    username,
                    msg_id,
                )

            except UsernameNotOccupied:
                bot.send_message(
                    message.chat.id,
                    "❌ **频道用户名不存在**",
                    reply_to_message_id=message.id,
                )

                return
            try:

                # 单条模式

                if "?single" in text:
                    bot.copy_message(
                        message.chat.id,
                        msg.chat.id,
                        msg.id,
                        reply_to_message_id=message.id,
                    )

                # 相册模式

                elif msg.media_group_id:
                    bot.copy_media_group(
                        message.chat.id,
                        msg.chat.id,
                        msg.id,
                        reply_to_message_id=message.id,
                    )


                # 普通消息

                else:
                    bot.copy_message(
                        message.chat.id,
                        msg.chat.id,
                        msg.id,
                        reply_to_message_id=message.id,
                    )


            except Exception:
                if acc is None:

                    bot.send_message(
                        message.chat.id,
                        "⚠️ **无法获取内容，需要 String Session**",
                        reply_to_message_id=message.id,
                    )

                    return

                handle_private(
                    message,
                    username,
                    msg_id,
                )

        time.sleep(3)


# ==========================
# Start Bot
# ==========================


print(
    "🤖 「存迹」Started..."
)

bot.run()