import os
import time

import pygame as pygame

from BddAgent import BddAgent
from Utils import Utils


class Main:

    @staticmethod
    def ad_hoc_temperature_tests(agent: BddAgent):
        input_folder = "input_folder/"
        for filename in os.listdir(input_folder):
            path = input_folder + filename
            role = "user" if filename[-5] == "r" else "system"
            print(f"adding message from file {path} with role {role}")
            agent.add_message_from_file(role=role, file_path=path)
            print("message added successfully")

    @staticmethod
    def ask_messages_from_files(agent: BddAgent):
        c = 1
        input_dir = input("Insert input directory name:\n")
        file_name = "placeholder"
        while file_name:
            # procedure ask for file name
            file_name = input(f"Insert name of file {c}. Insert empty to stop inserting:\n")
            if file_name == "":
                break
            while not os.path.exists(f"{input_dir}/{file_name}"):
                file_name = input(f"File {c} does not exist. Try again or insert empty to stop inserting:\n")
                if file_name == "":
                    break

            # procedure to ask for message's role
            role = input(f"Insert message's role or insert empty to reinsert filename {c}:\n")
            if role == "":
                continue
            while role not in ("system", "user", "assistant"):
                role = input(f"Invalid role. Try again or insert empty to reinsert filename {c}:\n")
                if role != "":
                    continue
            if file_name and role:
                file_path = f"{input_dir}/{file_name}"
                print(f"role: {role}, file_path: {file_path}")
                agent.add_message_from_file(role, file_path)
                c += 1
        print("file selection finished.")

    @staticmethod
    def run_chat(output_folder=None, temperature: float = 0):
        agent = BddAgent()
        c = 1
        if output_folder:
            os.makedirs(output_folder, exist_ok=True)
        if not output_folder:
            output_folder = input("Insert the target output file:\n")

        Main.ad_hoc_temperature_tests(agent)
        while c <= 5:
            try:
                print(f"running run {c}")
                agent.run(instruction="", model="gpt-4", temperature=temperature)
                # response saving
                response_content = agent.last_response.content
                Utils.strip_gherkin_formatting(response_content)
                output_file_path = f"{output_folder}/response_{c}.feature"
                Utils.string_to_file(output_file_path, response_content)
                print(f"Response was saved to file {output_file_path}")
                c += 1
            except Exception() as e:
                print("Error. Trying again in 15 seconds")
                time.sleep(15)

    @staticmethod
    def run_chat_with_files(output_folder=None):
        agent = BddAgent()
        c = 1
        if not output_folder:
            output_folder = input("Insert the target output file:\n")
        Main.ask_messages_from_files(agent)
        while c <= 5:
            try:
                agent.run(instruction="", model="gpt-4", save_response_to_message=False)
                # response saving
                response_content = agent.last_response.content
                Utils.strip_gherkin_formatting(response_content)
                output_file_path = f"{output_folder}/response_{c}.feature"
                Utils.string_to_file(output_file_path, response_content)
                print(f"Response was saved to file {output_file_path}")
                c += 1
            except Exception() as e:
                print("Error. Trying again in 15 seconds")
                time.sleep(15)
    @staticmethod
    def run_like_chat(agent: BddAgent, temp, output_folder=f"output_folder/", input_folder="input_folder/", seed=None):
        c = 1
        for filename in os.listdir(input_folder):
            path = input_folder + filename
            role = "user" if filename[-5] == "r" else "system"
            print(f"adding message from file {path} with role {role}")
            agent.add_message_from_file(role=role, file_path=path)
            print("message added successfully")
            if role == "system":
                print("Role is system. skipping response")
                continue
            while True:
                try:
                    print(f"agent running")
                    agent.run(instruction="", model="gpt-4", temperature=temp, save_response_to_message=True, seed=seed)
                    response_content = agent.last_response.content
                    Utils.strip_gherkin_formatting(response_content)
                    output_file_path = f"{output_folder}/response_{c}.feature"
                    Utils.string_to_file(output_file_path, response_content)
                    c += 1
                    print(f"Response was saved to file {output_file_path}")
                    break
                except Exception() as e:
                    print("Run failed. Trying again")
    @staticmethod
    def run(user_story_file):
        temperatures = [None]
        starting_run = 1
        final_run = 1
        for temperature in temperatures:
            for i in range(starting_run, final_run + 1):
                output_folder = f"output_folder/temperature_{temperature}/chat{i}"
                agent = BddAgent()
                os.makedirs(output_folder, exist_ok=True)
                Main.run_like_chat(agent=agent, output_folder=output_folder, temp=temperature)
                whole_chat_folder = f"{output_folder}/whole_chat"
                os.makedirs(whole_chat_folder, exist_ok=True)
                for c, message in enumerate(agent.messages):
                    Utils.string_to_file(f"{whole_chat_folder}/message_{c + 1}_role={message['role']}.txt",
                                         message["content"])


temperatures = [None]
starting_run = 1
final_run = 1
for temperature in temperatures:
    for i in range(starting_run, final_run + 1):
        output_folder = f"output_folder/temperature_{temperature}/chat{i}"
        agent = BddAgent()
        os.makedirs(output_folder, exist_ok=True)
        Main.run_like_chat(agent=agent, output_folder=output_folder, temp=temperature)
        whole_chat_folder = f"{output_folder}/whole_chat"
        os.makedirs(whole_chat_folder, exist_ok=True)
        for c, message in enumerate(agent.messages):
            Utils.string_to_file(f"{whole_chat_folder}/message_{c+1}_role={message['role']}.txt", message["content"])

# Indicador sonoro ao final do código
pygame.init()
pygame.mixer.music.load("decidemp3-14575.mp3")
pygame.mixer.music.play()

pygame.time.Clock().tick(10)
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)