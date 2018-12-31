#!/usr/bin/env python

from pydbus import SystemBus
from interaction.dbus import SERVICE_NAME

from gi.repository import GLib

from queue import Queue

class InteractionClient(object):

    def __init__(self):
        self.bus = SystemBus()
        self.loop = GLib.MainLoop()
        self.interaction_interface = self.bus.get(SERVICE_NAME, "/Interaction")
    def tell(self, text):
        self.interaction_interface.Tell(text)

    def ask(self, question_text, keyboard):
        answer_text_queue = Queue()

        question = self.bus.get(SERVICE_NAME, self.interaction_interface.Ask(question_text, keyboard))

        def signal_callback(answer_text):
            answer_text_queue.put(answer_text)
            self.loop.quit()

        question.AnswerReceived.connect(signal_callback)
        try:
            self.loop.run()
            answer_text  = answer_text_queue.get()
            return answer_text
        except KeyboardInterrupt:
            loop.quit()
