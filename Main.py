import os

from openai import OpenAI
from openai.pagination import SyncCursorPage
from openai.types.beta.threads import ThreadMessage

from BddAgent import BddAgent


class Main:
    @staticmethod
    def file_to_string(file_name: str):
        with open(file_name, "r", encoding="utf-8") as input_file:
            return "".join(input_file.readlines())

    @staticmethod
    def string_to_file(file_name: str, string: str):
        with open(file_name, "w", encoding="utf-8") as output_file:
            output_file.write(string)

    @staticmethod
    def main():
        os.environ["OPENAI_API_KEY"] = Main.file_to_string("key.txt")

        agent = BddAgent()
        agent.add_message(
            Main.file_to_string('input.txt')
        )
        agent.run()
        Main.string_to_file("ft1.feature", agent.last_message.content[0].text.value)
        return


Main.main()
