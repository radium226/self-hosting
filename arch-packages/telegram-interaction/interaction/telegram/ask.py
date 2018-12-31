#!/usr/bin/env python

class Ask(object):

    def __init__(self, question_text, keyboard, answer_callback):
        self.question_text = question_text
        self.keyboard = keyboard
        self.answer_callback = answer_callback
