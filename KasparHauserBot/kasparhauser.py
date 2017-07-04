from uuid import uuid4

import logging
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import InlineQueryResultArticle
from telegram import InputTextMessageContent
from telegram import ParseMode
from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import InlineQueryHandler
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import escape_markdown


class KasparHauser:

    def __init__(self, key, google_search):

        self.updater = Updater(key)

        self.updater.dispatcher.add_error_handler(self.__handle_error)

        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self.__handle_text_input))
        self.updater.dispatcher.add_handler(InlineQueryHandler(self.__handle_inline_query))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.__handle_callback_query))

        self.updater.dispatcher.add_handler(CommandHandler('help', self.__help_handler))
        self.updater.dispatcher.add_handler(CommandHandler('about', self.__about_handler))
        self.updater.dispatcher.add_handler(CommandHandler('start', self.__start_handler))

        self.updater.dispatcher.add_handler(CommandHandler('search', self.__search_handler))
        self.updater.dispatcher.add_handler(CommandHandler('lmgtfy', self.__search_handler))

        self.google_search = google_search

    def start(self):
        self.updater.start_polling()
        self.updater.idle()

    # region Handlers of base types
    def __handle_error(self, bot, update, error):
        logging.log(logging.DEBUG, 'Update "%s" caused error "%s"' % (update, error))

    def __handle_text_input(self, bot, update):
        update.message.reply_text('You typed this text: {}'.format(update.message.text))

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

    # endregion

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

    @run_async
    def __search_handler(self, bot, update):

        result = self.google_search.search(search_term=update.message.text
                                           .replace('/search', '', 1)
                                           .replace('/lmgtfy', '', 1), num=5)

        logging.log(logging.DEBUG, 'Search called')

        search_information = result['searchInformation']

        search_time = search_information['formattedSearchTime']
        total_results = search_information['formattedTotalResults']

        update.message.reply_text("Search time: %s, total results: %s" % (search_time, total_results))

        spelling = result.get('spelling')

        if spelling is not None:
            corrected_spelling = spelling['correctedQuery']
            update.message.reply_text("Corrected query: %s" % (corrected_spelling))

        items = result['items']

        for i, item in enumerate(items):
            update.message.reply_text("*%d.* %s\n\n"
                                      "%s\n\n"
                                      "%s" % (i + 1, escape_markdown(item['title']),
                                              escape_markdown(item['formattedUrl']),
                                              escape_markdown(item['snippet'])),
                                      parse_mode=ParseMode.MARKDOWN)






