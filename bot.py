import logging
import sqlite3
from datetime import datetime
import random
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# 配置
TOKEN = "8231003819:AAGaSNhTFbxN0CVjg5oXD_VJ0MrF_v11ucM"  # 替换为@BotFather的Token
PLATFORM_URL = "https://jdyl.me/?ref=tg"  # 九鼎娱乐链接

# SQLite数据库
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, messages INTEGER, last_active TEXT, vip_status INTEGER)''')
    conn.commit()
    conn.close()

# 欢迎消息
WELCOME_TEXT = f"""🔥欢迎加入【九鼎娱乐东南亚福利群】！
🎰电子福利：注册送$10体验金，玩PG老虎机爆大奖！{PLATFORM_URL}
🐟捕鱼技巧：每日高爆率分享，金币赠送！
⚽体育信号：泰超/英超预测，胜率65%+！
🎁入群抽$20 USDT！规则：禁广告/私聊，18+理性娱乐。问题@admin。
命令：/tips 获取信号，/subscribe 订阅VIP"""

# 信号
TIPS_EXAMPLES = [
    "📊泰超：曼谷联胜 @1.85",
    "🐟捕鱼技巧：火箭炮瞄鲨鱼群，高爆率5000倍！",
    "🎰PG《Fortune Tiger》免费10转，注册领！"
]

# 欢迎命令
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, messages, last_active, vip_status) VALUES (?, ?, ?, ?)",
              (user_id, 0, datetime.now().isoformat(), 0))
    conn.commit()
    conn.close()
    await update.message.reply_text(WELCOME_TEXT)

# 信号命令
async def tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tip = random.choice(TIPS_EXAMPLES)
    await update.message.reply_text(tip)

# 订阅命令
async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, messages, last_active, vip_status) VALUES (?, ?, ?, ?)",
              (user_id, 0, datetime.now().isoformat(), 0))
    c.execute("UPDATE users SET messages = messages + 1, last_active = ? WHERE user_id = ?",
              (datetime.now().isoformat(), user_id))
    conn.commit()
    conn.close()
    
    keyboard = [
        [InlineKeyboardButton("10 USDT (VIP信号)", callback_data="pay_10"),
         InlineKeyboardButton("50 USDT (月卡)", callback_data="pay_50")],
        [InlineKeyboardButton("查看统计", callback_data="stats")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("选择订阅计划（充值后享高级信号+福利）：", reply_markup=reply_markup)

# 支付按钮处理
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if query.data == "pay_10":
        await query.edit_message_text("请转10 USDT到地址：TX123456789...\n支付后发送/confirm激活VIP！")
    elif query.data == "pay_50":
        await query.edit_message_text("请转50 USDT到地址：TX987654321...\n支付后发送/confirm激活月卡！")
    elif query.data == "stats":
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT messages, last_active, vip_status FROM users WHERE user_id = ?", (user_id,))
        stats = c.fetchone()
        conn.close()
        if stats is None:
            stats_text = "你还没有注册，请先发送 /start 命令！"
        else:
            stats_text = f"你的统计：\n消息数: {stats[0]}\n最后活跃: {stats[1]}\nVIP状态: {'是' if stats[2] else '否'}"
        await query.edit_message_text(stats_text)

# 支付确认
async def confirm_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, messages, last_active, vip_status) VALUES (?, ?, ?, ?)",
              (user_id, 0, datetime.now().isoformat(), 0))
    c.execute("UPDATE users SET vip_status = 1, messages = messages + 1, last_active = ? WHERE user_id = ?",
              (datetime.now().isoformat(), user_id))
    conn.commit()
    conn.close()
    await update.message.reply_text("支付确认！解锁九鼎娱乐VIP信号+捕鱼金币。发送/tips获取福利！")

# 主函数
def main():
    # Get token from environment variable with fallback
    bot_token = os.environ.get('BOT_TOKEN', TOKEN)
    
    # Raise error if token is empty
    if not bot_token:
        raise RuntimeError("Bot token not provided! Please set BOT_TOKEN environment variable.")
    
    init_db()
    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tips", tips))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("confirm_payment", confirm_payment))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("九鼎娱乐Bot启动中...")
    app.run_polling()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
