import os
import time
from pathlib import Path

from openai import OpenAI
from openai.pagination import SyncCursorPage
from openai.types.beta.threads import ThreadMessage

from BddAgent import BddAgent


class Main:
    @classmethod
    def file_to_string(cls, file_name: str):
        with open(file_name, "r", encoding="utf-8") as input_file:
            return "".join(input_file.readlines())

    @classmethod
    def string_to_file(cls, file_name: str, string: str):
        with open(file_name, "w", encoding="utf-8") as output_file:
            output_file.write(string)

    @classmethod
    def user_story_to_feature(cls, input_file_path: str, output_file_path: str, instruction: str):
        print(f"Processing input file {input_file_path}")
        print("Creating new agent instance")
        agent = BddAgent()
        print("New agent created successfully. Adding message to thread")
        agent.add_message(cls.file_to_string(input_file_path))
        print("Input file message to the API successfully. Attempting to run the thread")
        agent.run(instructions=instruction)
        print("Thread run successfully. Writing to output file")
        cls.string_to_file(output_file_path, agent.last_message.content[0].text.value)

    @classmethod
    def main(cls):
        output_folder_path = "output_folder/"
        input_folder_path = "input_folder/"
        instruction = cls.file_to_string("instructions.txt")

        os.environ["OPENAI_API_KEY"] = cls.file_to_string("key.txt")
        cls.string_to_file(f"{output_folder_path}instruction_used.txt", instruction)
        input_file_name_list = os.listdir(input_folder_path)
        for i, input_file_name in enumerate(input_file_name_list):
            print(f"================== new file: {i+1} out of {len(input_file_name_list)}")
            for j in range(1, 6):
                print(f"======================= new iteration: {j} out of 5")
                input_file_path = f"{input_folder_path}{input_file_name}"
                output_file_path = f"{output_folder_path}{Path(input_file_name).stem}{j}.feature"
                if os.path.exists(output_file_path):
                    print("File already exists. Continuing")
                    continue
                while True:
                    try:
                        cls.user_story_to_feature(input_file_path, output_file_path, instruction)
                        break
                    except Exception as e:
                        print(f"Error processing input file {input_file_path}.")
                        print("Waiting 45 seconds before trying again")
                        time.sleep(45)
                        print("trying again.")


Main.main()
