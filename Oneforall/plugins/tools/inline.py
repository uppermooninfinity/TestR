from pyrogram import Client
from pyrogram.types import ChatPrivileges

from Oneforall import app


def build_msg(action, admin, target, title=None):
    text = (
        f"✨ <b>{action}</b>\n\n"
        f"👑 <b>Admin:</b> {admin.mention}\n"
        f"👤 <b>User:</b> {target.mention}\n"
    )

    if title:
        text += f"🏷 <b>Title:</b> {title}\n"

    text += "\n──────────────"
    return text


@app.on_chat_member_updated()
async def admin_change_handler(client, message):

    old = message.old_chat_member
    new = message.new_chat_member

    if not old or not new:
        return

    chat_id = message.chat.id
    admin = message.from_user
    target = new.user

    old_priv = old.privileges
    new_priv = new.privileges

    old_title = old.custom_title
    new_title = new.custom_title

    # 🔹 Promotion
    if old_priv is None and new_priv is not None:
        text = build_msg("Promoted", admin, target, new_title or "No Title")
        await client.send_message(chat_id, text)
        return

    # 🔹 Demotion
    if old_priv is not None and new_priv is None:
        text = build_msg("Demoted", admin, target)
        await client.send_message(chat_id, text)
        return

    # 🔹 Title Change
    if old_title != new_title:
        text = build_msg("Title Changed", admin, target, new_title or "No Title")
        await client.send_message(chat_id, text)
        return
