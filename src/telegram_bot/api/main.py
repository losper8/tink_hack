from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, \
    CallbackQueryHandler

from embeddings.api.schema import SearchRequest
from rag_pipeline.domain.rag_functions import rag_final_response
from telegram_bot.api.config.telegram_bot_config import telegram_bot_config


async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = SearchRequest(text=update.message.text)
    output, details = await rag_final_response(request=response, encoding_model='gigachat', n_results=10,
                                               include_embeddings=False, ids=[])
    keyboard = [[InlineKeyboardButton("Подробности", callback_data='details')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=output, reply_markup=reply_markup)
    context.user_data['details'] = details
    context.user_data['question'] = response.text


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'details':
        details = context.user_data.get('details', "Нет подробностей.")[:4000]
        await context.bot.send_message(chat_id=update.effective_chat.id, text=details)

app = ApplicationBuilder().token(telegram_bot_config.TOKEN).build()

ask_question_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), ask_question)
app.add_handler(ask_question_handler)

button_handler = CallbackQueryHandler(button_handler)
app.add_handler(button_handler)


app.run_polling()
