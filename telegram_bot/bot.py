import os
import json
import requests
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ============================================================
# CONFIG
# ============================================================
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# Paths
PRODUCTS_FILE = "data/latest_products.json"
MEMORY_FILE = "learning/memory.json"

# ============================================================
# HELPERS
# ============================================================
def load_products():
    try:
        with open(PRODUCTS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_feedback(product_id, action):
    """Save user feedback for learning"""
    memory = {}
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            memory = json.load(f)
    
    if "feedbacks" not in memory:
        memory["feedbacks"] = []
    
    memory["feedbacks"].append({
        "product_id": product_id,
        "action": action,  # "approve" or "reject"
        "timestamp": datetime.now().isoformat()
    })
    
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

# ============================================================
# BOT COMMANDS
# ============================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 <b>Dropshipping AI Agent Bot</b>\n\n"
        "Commands:\n"
        "/daily - Get today's top 5 products\n"
        "/stats - Learning stats\n"
        "/help - Show this message\n\n"
        "When you get products, you can:\n"
        "✅ Approve - Product is good\n"
        "❌ Reject - Product is not good\n\n"
        "The AI will learn from your feedback!",
        parse_mode="HTML"
    )

async def daily_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    products = load_products()
    
    if not products:
        await update.message.reply_text("❌ No products found. Run the scanner first!")
        return
    
    message = "🏆 <b>TOP 5 PRODUCTS FOR TODAY</b>\n\n"
    
    for i, p in enumerate(products, 1):
        message += f"{i}. <b>{p.get('name', 'Unknown')}</b>\n"
        message += f"   💰 Price: AED {p.get('price', 0)}\n"
        message += f"   📊 Score: {p.get('score', 0)}/100\n"
        message += f"   ✅ Factors: {', '.join(p.get('factors_used', []))}\n\n"
    
    # Create inline buttons for feedback
    keyboard = []
    for i, p in enumerate(products[:3], 1):  # Only top 3 for feedback
        keyboard.append([
            InlineKeyboardButton(f"✅ Approve #{i}", callback_data=f"approve_{p.get('id', i)}"),
            InlineKeyboardButton(f"❌ Reject #{i}", callback_data=f"reject_{p.get('id', i)}")
        ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(message, parse_mode="HTML", reply_markup=reply_markup)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            memory = json.load(f)
        feedbacks = memory.get("feedbacks", [])
        
        approvals = len([f for f in feedbacks if f['action'] == 'approve'])
        rejects = len([f for f in feedbacks if f['action'] == 'reject'])
        
        message = f"📊 <b>Learning Statistics</b>\n\n"
        message += f"Total feedbacks: {len(feedbacks)}\n"
        message += f"✅ Approvals: {approvals}\n"
        message += f"❌ Rejects: {rejects}\n"
        
        if len(feedbacks) > 0:
            message += f"\nAccuracy: {approvals/(approvals+rejects)*100:.1f}%"
    else:
        message = "No learning data yet. Start giving feedback!"
    
    await update.message.reply_text(message, parse_mode="HTML")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    action, product_id = data.split("_")
    
    save_feedback(product_id, action)
    
    if action == "approve":
        await query.edit_message_text(f"✅ Product {product_id} approved! AI will learn from this.")
    else:
        await query.edit_message_text(f"❌ Product {product_id} rejected. AI will avoid similar products.")

# ============================================================
# MAIN
# ============================================================
def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("daily", daily_products))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    print("🤖 Telegram Bot started!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
