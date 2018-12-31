#!/usr/bin/env python

from uuid import uuid4

from pydbus.generic import signal


class QuestionInterface(object):
    """
        <node>
            <interface name='com.github.radium226.Question'>
                <signal name='AnswerReceived'>
                    <arg type='s' />
                </signal>
            </interface>
        </node>
    """

    AnswerReceived = signal()

    def __init__(self, bus):
        self.bus = bus
        self.uuid = uuid4()
