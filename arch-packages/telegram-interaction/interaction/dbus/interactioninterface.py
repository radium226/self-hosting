#!/usr/bin/env python

from .questioninterface import QuestionInterface

class InteractionInterface(object):
    """
        <node>
            <interface name='com.github.radium226.Interaction'>
                <method name='Tell'>
                    <arg name='keys' type='s' direction='in'/>
                </method>
                <method name='Ask'>
                    <arg name='question_text' type='s' direction='in'/>
                    <arg name='keyboard' type='as' direction='in'/>
                    <arg name='question_path' type='o' direction='out'/>
                </method>
            </interface>
        </node>
    """

    def __init__(self, bus, bot):
        self.bus = bus
        self.bot = bot

    def Tell(self, text):
        self.bot.tell(text)

    def Ask(self, question_text, keyboard):
        print(f"question_text={question_text}")
        print(f"keyboard={keyboard}")

        question_interface = QuestionInterface(self.bus)
        question_interface_path = f"/questions/{str(question_interface.uuid)}".replace("-", "_")
        print(f"question_interface_path={question_interface_path}")
        registration = self.bus.register_object(question_interface_path, question_interface, None)

        def answer_callback(text):
            question_interface.AnswerReceived.emit(text)
            registration.unregister()

        self.bot.ask(question_text, keyboard, answer_callback)
        return question_interface_path
