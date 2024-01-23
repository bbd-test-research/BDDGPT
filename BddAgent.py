import os
import random
import time

from openai import OpenAI

from Utils import Utils


class BddAgent:

    def __init__(self):
        os.environ["OPENAI_API_KEY"] = Utils.file_to_string("key.txt")
        self.client = OpenAI()
        self.output_folder_path = "output_folder/"
        self.input_folder_path = "input_folder/"
        self.instruction = Utils.file_to_string("instructions.txt")

    def run(self, iterations_per_input, instruction=None, model="gpt-3.5-turbo-1106"):
        if instruction is None:
            instruction = self.instruction
        Utils.string_to_file(f"{self.output_folder_path}instruction_used.txt", self.instruction)
        # if the stream parameter is not set to true, the completion executes synchronously
        file_names = os.listdir(self.input_folder_path)
        for file_name in file_names:
            c = 0

            messages = [{"role": "user", "content": Utils.file_to_string(f"{self.input_folder_path}{file_name}")}]
            if instruction:
                messages.append({"role": "system", "content": instruction})
                messages.reverse()
            print("messages: ", messages)
            while c < iterations_per_input:
                output_path = f"{self.output_folder_path}{os.path.splitext(file_name)[0]}_{c + 1}.feature"
                try:
                    completion = self.client.chat.completions.create(
                        model=model,
                        messages=messages,
                        # messages=[{"role": "user", "content": "Say this is a test"}],
                        temperature=0,
                    )
                    Utils.string_to_file(output_path, completion.choices[0].message.content)
                    c += 1
                except Exception as e:
                    print(f"Error!")
                    print(e)
                    print("Trying again in 30 seconds")
                    time.sleep(30)
