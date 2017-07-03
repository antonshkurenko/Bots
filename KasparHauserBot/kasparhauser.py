from uuid import uuid4

from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import InlineQueryResultArticle
from telegram import InputTextMessageContent
from telegram.ext import CallbackQueryHandler
from telegram.ext import Filters
from telegram.ext import InlineQueryHandler
from telegram.ext import MessageHandler
from telegram.ext import Updater


class KasparHauser:

    command_handlers = {}

    def __init__(self, key):

        self.updater = Updater(key)

        self.updater.dispatcher.add_error_handler(self.__handle_error)

        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self.__handle_text_input))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.command, self.__handle_command_input))
        self.updater.dispatcher.add_handler(InlineQueryHandler(self.__handle_inline_query))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.__handle_callback_query))

        self.command_handlers["/help"] = self.__help_handler
        self.command_handlers["/about"] = self.__about_handler
        self.command_handlers["/start"] = self.__start_handler

    def start(self):
        self.updater.start_polling()
        self.updater.idle()

    def __handle_error(self, bot, update, error):
        print('Update "%s" caused error "%s"' % (update, error))

    def __handle_text_input(self, bot, update):
        update.message.reply_text('You typed this text: {}'.format(update.message.text))

    def __handle_command_input(self, bot, update):

        command = self.command_handlers.get(update.message.text)

        if command is not None:
            command(bot, update)
        else:
            update.message.reply_text('Unknown command: %s\nUse /help, to check all available commands' % update.message.text)

    def __handle_inline_query(self, bot, update):

        query = update.inline_query.query
        results = list()

        results.append(InlineQueryResultArticle(id=uuid4(),
                                                title="Caps",
                                                input_message_content=InputTextMessageContent(
                                                    query.upper())))

        results.append(InlineQueryResultArticle(id=uuid4(),
                                                title="Simple",
                                                input_message_content=InputTextMessageContent(
                                                    query)))

        update.inline_query.answer(results)


    def __handle_callback_query(self, bot, update):
        query = update.callback_query

        bot.edit_message_text(text="Selected option: %s" % query.data,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)


    def __help_handler(self, bot, update):
        update.message.reply_text("/help -- help\n"
                                  "/about -- about\n"
                                  "/start -- keyboard test\n"
                                  "\n"
                                  "Also inline queries")


    def __about_handler(self, bot, update):
        update.message.reply_text("Here will be about!")


    def __start_handler(self, bot, update):

        keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                     InlineKeyboardButton("Option 2", callback_data='2')],

                    [InlineKeyboardButton("Option 3", callback_data='3')]]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('Please choose:', reply_markup=reply_markup)





