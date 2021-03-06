from telegram import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
                      InlineKeyboardButton)

from .models import Menu


def test(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat.id, text='test message')


def start(update, context):
    chat = update.effective_chat
    buttons = ReplyKeyboardMarkup([
        ['стартовое меню']
    ], resize_keyboard=True)
    context.bot.send_message(
        chat.id,
        text='Bot is started',
        reply_markup=buttons
    )


def inline(update, context):
    chat = update.effective_chat
    buttons = [
        [InlineKeyboardButton('Button 1', callback_data='one', ),
         InlineKeyboardButton('Button 1', callback_data='two', )]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text("Please choose:", reply_markup=reply_markup)


def callback_test(update, context):
    query = update.callback_query
    query.answer()
    buttons = [
        [InlineKeyboardButton('Button 1', callback_data='one', ),
         InlineKeyboardButton('Button 1', callback_data='two', )]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    query.edit_message_text(
        text=f"Change option: {query.data}",
        reply_markup=reply_markup
    )


def post(update, context):
    chat = update.effective_chat
    buttons = [
        [InlineKeyboardButton('Button 1', callback_data='one', ),
         InlineKeyboardButton('Button 1', callback_data='two', )]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text("POST:", reply_markup=reply_markup)


def generate_keyboard(buttons: list) -> ReplyKeyboardMarkup:
    mid = len(buttons) // 2
    current_buttons = [button.slug.value for button in buttons]
    reply_markup = ReplyKeyboardMarkup(
        [
            current_buttons[mid:],
            current_buttons[:mid]
        ],
        resize_keyboard=True
    )
    return reply_markup


def generate_inline_keyboard(buttons: list) -> InlineKeyboardMarkup:
    mid = len(buttons) // 2
    current_buttons = [
        InlineKeyboardButton(
            button.name, callback_data=button.slug.value
        ) for button in buttons
    ]
    buttons = [
        current_buttons[mid:],
        current_buttons[:mid]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    return reply_markup


def command(update, context, slug: str) -> None:
    chat = update.effective_chat
    menu = Menu.objects.get(slug__value=slug)
    buttons = menu.buttons.all()
    reply_markup = generate_keyboard(buttons)
    if menu.content:
        context.bot.send_photo(chat.id, menu.content.image)
        context.bot.send_message(
            chat.id,
            text=menu.content.text,
            reply_markup=reply_markup,
        )
    else:
        context.bot.send_message(
            chat.id,
            text=menu.name,
            reply_markup=reply_markup,

        )


def chat(update, context, slug):
    chat = update.effective_chat
    menu = Menu.objects.get(slug__value=slug)
    buttons = menu.content.buttons.all()
    reply_markup = generate_inline_keyboard(buttons)
    if menu.content.image:
        context.bot.send_photo(chat.id, menu.content.image)
    context.bot.send_message(
        chat.id,
        text=menu.content.text,
        reply_markup=reply_markup,
    )
