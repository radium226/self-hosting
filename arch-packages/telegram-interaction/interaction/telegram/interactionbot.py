#!/usr/bin/env python

from .ask import Ask
from .tell import Tell

from telegram import Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
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
                else:
                    raise Exception(f"Unknown action {action}")

        self.action_thread = Thread(target=action_thread_target)
        self.action_thread.start()

    def _do_tell(self, text, keyboard):
        print(f"keyboard={keyboard}")
        reply_markup = ReplyKeyboardRemove()
        if keyboard:
            reply_markup = ReplyKeyboardMarkup([keyboard])

        self.bot.send_message(self.telegram_chat_id, text, reply_markup=reply_markup)

    def _do_ask(self, question_text, keyboard, answer_callback):
        message_queue = Queue()
        def handler_callback(bot, update):
            message = update.message
            print(f" ----> {message.text}")
            message_queue.put(message)

        updater = Updater(self.telegram_token)
        updater.dispatcher.add_handler(MessageHandler(Filters.text, handler_callback))
        updater.start_polling()

        self._do_tell(question_text, keyboard)
        message = message_queue.get()
        updater.stop()
        self._do_tell("Ok! ", None)
        answer_callback(message.text)

    def tell(self, text, keyboard = None):
        self.action_queue.put(Tell(text, keyboard))

    def ask(self, question_text, keyboard, answer_callback):
        self.action_queue.put(Ask(question_text, keyboard, answer_callback))
