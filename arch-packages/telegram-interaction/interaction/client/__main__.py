#!/usr/bin/env python

from interaction.client import InteractionClient

import argparse

import sys

from pathlib import Path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action") # this line changed

    tell_parser = subparsers.add_parser("tell")
    tell_parser.add_argument("--text", required=True)
    def tell(client, args):
        client.tell(args.text)

    ask_parser = subparsers.add_parser("ask")
    ask_parser.add_argument("--text", required=True, dest="question_text")
    ask_parser.add_argument("--keyboard", nargs='*', default=[])
    def ask(client, args):
        print(client.ask(args.question_text, args.keyboard))

    test_parser = subparsers.add_parser("test")
    test_parser.add_argument("--text", required=True, dest="question_text")
    def test(client, args):
        answer_text = client.ask(args.question_text, keyboard=["Oui", "Non"])
        if answer_text == "Oui":
            sys.exit(0)
        else:
            sys.exit(1)

    share_parser = subparsers.add_parser("share")
    share_parser.add_argument("--file", required=True, dest="file_path")
    def share(client, args):
        client.share(Path(args.file_path))

    actions = {
        "ask": ask,
        "tell": tell,
        "test": test,
        "share": share
    }

    args = parser.parse_args()
    client = InteractionClient()
    actions[args.action](client, args)
