from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import CallbackContext

from db import add_or_update_user, get_user_lang, set_user_lang

# Translation dictionary
TEXTS = {
    "uz": {
        "greet_new": "Salom {name}, botga xush kelibsiz! 👋",
        "greet_back": "Qaytganingiz bilan, {name}!",
        "choose_episode": "Qaysi episodni ko‘rmoqchisiz?",
        "episode_chosen": "Siz {num}-episodni tanladingiz 🎬",
        "main_menu_text": "Asosiy sahifa",
        "language_prompt": "Tilni tanlang / Tilni o‘zgartiring:",
        "language_set": "Til {lang} ga o‘zgartirildi.",
        "help_text": "{name}, qanday yordam kerak?",
        "back": "⬅️ Orqaga",
        "language_label": "Til tugmasi",
        "main_button": "Bosh Sahifa",
    },
    "en": {
        "greet_new": "Hello {name}, welcome to the bot! 👋",
        "greet_back": "Welcome back, {name}!",
        "choose_episode": "Which episode would you like to watch?",
        "episode_chosen": "You chose Episode {num} 🎬",
        "main_menu_text": "Main menu",
        "language_prompt": "Choose language / Change language:",
        "language_set": "Language changed to {lang}.",
        "help_text": "{name}, how can I help?",
        "back": "⬅️ Back",
        "language_label": "Til tugmasi",
        "main_button": "Main Menu",
    }
}

LANG_LABEL = {"uz": "O‘zbekcha", "en": "English"}

def t(user_lang: str, key: str, **kwargs) -> str:
    template = TEXTS.get(user_lang, TEXTS["uz"]).get(key, "")
    return template.format(**kwargs)

async def start_handler(update: Update, context: CallbackContext):
    user = update.message.from_user
    # default lang: uz
    add_or_update_user(user.id, user.full_name, user.username, lang=get_user_lang(user.id) or "uz")

    lang = get_user_lang(user.id)
    users = ReplyKeyboardMarkup(
        keyboard=[
            [TEXTS[lang]["main_button"], TEXTS[lang]["language_label"]],
        ],
        resize_keyboard=True
    )

    
    users_data = get_user_lang(user.id)
   
    await update.message.reply_text(
        text=t(lang, "greet_new", name=user.full_name),
        reply_markup=users
    )

async def help_handler(update: Update, context: CallbackContext):
    lang = get_user_lang(update.message.from_user.id)
    await update.message.reply_text(
        text=t(lang, "help_text", name=update.message.from_user.full_name)
    )

async def text_handler(update: Update, context: CallbackContext):
    text = update.message.text
    user_id = update.message.from_user.id
    lang = get_user_lang(user_id)

    
    if text == TEXTS[lang]["main_button"]:
        return await main_menu_handler(update, context)

    if text == TEXTS[lang]["language_label"]:
        return await language_toggle_handler(update, context)

    
    await update.message.reply_text(text)

async def photo_handler(update: Update, context: CallbackContext):
    
    photo = update.message.photo[-1].file_id
    await update.message.reply_photo(photo)

async def main_menu_handler(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    lang = get_user_lang(user_id)

    keyboard = [
        [InlineKeyboardButton("Episode 1 🎬", callback_data="ep_1"),
         InlineKeyboardButton("Episode 2 🎬", callback_data="ep_2")],
        [InlineKeyboardButton("Episode 3 🎬", callback_data="ep_3")],
        [InlineKeyboardButton(t(lang, "back"), callback_data="back_to_home")]
    ]
    reply = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(t(lang, "choose_episode"), reply_markup=reply)

async def language_toggle_handler(update: Update, context: CallbackContext):
    """Show inline buttons to pick language"""
    user_id = update.message.from_user.id
    lang = get_user_lang(user_id)

    keyboard = [
        [InlineKeyboardButton("O‘zbekcha", callback_data="set_lang_uz"),
         InlineKeyboardButton("English", callback_data="set_lang_en")]
    ]
    reply = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(t(lang, "language_prompt"), reply_markup=reply)

async def callback_query_handler(update: Update, context: CallbackContext):
    """Handle inline button clicks"""
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    lang = get_user_lang(user_id)

    
    await query.answer()

    if data.startswith("ep_"):
        
        num = data.split("_")[1]
        
        text = t(lang, "episode_chosen", num=num)
        await query.edit_message_text(text)
        return

    if data == "back_to_home":
        
        lang = get_user_lang(user_id)
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[TEXTS[lang]["main_button"], TEXTS[lang]["language_label"]]],
            resize_keyboard=True
        )
        await query.edit_message_text(t(lang, "main_menu_text"))
        await query.message.reply_text(" ", reply_markup=keyboard)
        return

    if data.startswith("set_lang_"):
        new_lang = data.split("_")[2]
        set_user_lang(user_id, new_lang)
        
        text = t(new_lang, "language_set", lang=LANG_LABEL[new_lang])
        await query.edit_message_text(text)


from db import get_user_lang as _get_user_lang
def get_user_lang(user_id):
    return _get_user_lang(user_id)
