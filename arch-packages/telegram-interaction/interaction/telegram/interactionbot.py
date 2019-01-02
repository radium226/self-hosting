#!/usr/bin/env python

from .ask import Ask
from .tell import Tell
from .share import Share

import telegram
from telegram import Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from queue import Queue

from threading import Thread

class InteractionBot(object):

    def __init__(self, telegram_token, telegram_chat_id):
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id
        self.bot = Bot(self.telegram_token)
        self.action_queue = Queue()

        def action_thread_target():
            while True:
                action = self.action_queue.get()
                if isinstance(action, Ask):
                    self._do_ask(action.question_text, action.keyboard, action.answer_callback)
                elif isinstance(action, Tell):
                    self._do_tell(action.text, action.keyboard)
                elif isinstance(action, Share):
                    self._do_share(action.file_path)
                else:
                    raise Exception(f"Unknown action {action}")

        self.action_thread = Thread(target=action_thread_target)
        self.action_thread.start()

    def _do_tell(self, text, keyboard):
        try:
            reply_markup = ReplyKeyboardRemove()
            if keyboard:
                reply_markup = ReplyKeyboardMarkup([keyboard])

            self.bot.send_message(self.telegram_chat_id, text, reply_markup=reply_markup, parse_mode=telegram.ParseMode.HTML)
        except Exception as e:
            print(e)

    def _do_ask(self, question_text, keyboard, answer_callback, answer_timeout=30, default_answer_text=None):
        message_queue = Queue()
        def handler_callback(bot, update):
            message = update.message
            message_queue.put(message)

        updater = Updater(self.telegram_token)
        updater.dispatcher.add_handler(MessageHandler(Filters.text, handler_callback))
        updater.start_polling()

        self._do_tell(question_text, keyboard)
        message = None
        try:
            message = message_queue.get(timeout=answer_timeout)
        except:
            pass
        updater.stop()
        if message:
            self._do_tell("Ok! ", None)
            answer_callback(message.text)
        else:
            self._do_tell("Trop tard :(", None)
            answer_callback(default_answer_text if default_answer_text else keyboard[0] if len(keyboard) > 0 else "")


    def _do_share(self, file_path):
        self.bot.send_document(self.telegram_chat_id, document=file_path.open("rb"))

    def tell(self, text, keyboard = None):
        self.action_queue.put(Tell(text, keyboard))

    def ask(self, question_text, keyboard, answer_callback):
        self.action_queue.put(Ask(question_text, keyboard, answer_callback))

    def share(self, file_path):
        self.action_queue.put(Share(file_path))
