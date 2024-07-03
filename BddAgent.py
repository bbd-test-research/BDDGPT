import os
import time

from openai import OpenAI

from Utils import Utils


class BddAgent:

    def __init__(self, use_instruction=False):
        os.environ["OPENAI_API_KEY"] = Utils.file_to_string("key.txt")
        self.client = OpenAI()
        self.output_folder_path = "output_folder/"
        self.input_folder_path = "input_folder/"
        if use_instruction:
            self.instruction = Utils.file_to_string("input_folder/instructions.txt")
        else:
            self.instruction = ""
        self.messages = []
        self.last_run = None
        self.last_response = None

    def add_message(self, role, content):
        self.messages.insert(0, {"role": role, "content": content})

    def append_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def append_message_from_file(self, role, file_path):
        self.append_message(role, Utils.file_to_string(file_path))

    def add_message_from_file(self, role, file_path):
        self.add_message(role, Utils.file_to_string(file_path))

    def run(self, instruction=None, model="gpt-3.5-turbo-1106", save_response_to_message=True, temperature=0, seed=None):
        """
        :param seed:
        :param instruction: overrides the agent's instruction
        :param model: defaults to gpt-3.5-turbo-1106.
        :param save_response_to_message: defaults to True. Whether to add the response to the agent's messages.
        :param temperature: the temperature hyperparameter of the run. determines how random the output will be from 0 to 1
        :return:
        """
        if instruction is None:
            instruction = self.instruction
        # The user may want to have no custom instruction.
        # In this case, there's no point adding an empty message
        if instruction != "":
            self.add_message("system", instruction)
            # documents instruction used
            Utils.string_to_file(f"{self.output_folder_path}instruction_used.txt", self.instruction)
        run_executed = False
        while not run_executed:
            try:
                if seed is None:
                    self.last_run = self.client.chat.completions.create(
                        model=model,
                        messages=self.messages,
                    )
                else:
                    self.last_run = self.client.chat.completions.create(
                        model=model,
                        messages=self.messages,
                        temperature=temperature,
                        seed=seed
                    )
                run_executed = True
            except Exception as e:
                print(f"Error!")
                print(e)
                print("Trying again in 30 seconds")
                time.sleep(30)
        self.last_response = self.last_run.choices[0].message
        if save_response_to_message:
            self.add_message(self.last_response.role, self.last_response.content)

    def run_old(self, iterations_per_input, instruction=None, model="gpt-3.5-turbo-1106", extra_messages=None):
        if instruction is None:
            instruction = self.instruction
        Utils.string_to_file(f"{self.output_folder_path}instruction_used.txt", self.instruction)
        # if the stream parameter is not set to true, the completion executes synchronously
        file_names = os.listdir(self.input_folder_path)
        for file_name in file_names:
            c = 0
            messages = [{"role": "user", "content": Utils.file_to_string(f"{self.input_folder_path}{file_name}")}]
            for m in extra_messages:
                messages.append({"role": "system", "content": m})
            if instruction:
                print("Instruction to be added.")
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
                        seed=0,

                    )
                    Utils.string_to_file(output_path, completion.choices[0].message.content)
                    c += 1
                except Exception as e:
                    print(f"Error!")
                    print(e)
                    print("Trying again in 30 seconds")
                    time.sleep(30)
