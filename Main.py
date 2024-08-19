import os
import argparse

from BddAgent import BddAgent
from Utils import Utils


class Main:

    @staticmethod
    def add_initial_messages(agent: BddAgent, message_1_path: str, message_2_path: str):
        # Adiciona a primeira mensagem a partir do arquivo message_1_response=user.txt
        print(f"adding initial message from file {message_1_path} with role user")
        agent.add_message_from_file(role="user", file_path=message_1_path)
        print("message 1 added successfully")

        # Adiciona a segunda mensagem a partir do arquivo especificado externamente
        print(f"adding second message from file {message_2_path} with role system")
        agent.add_message_from_file(role="system", file_path=message_2_path)
        print("message 2 added successfully")

    @staticmethod
    def run_like_chat(agent: BddAgent, temp, message_1_path: str, message_2_path: str, output_folder=f"output_folder/",
                      seed=None):
        # Adiciona as mensagens iniciais
        Main.add_initial_messages(agent, message_1_path, message_2_path)

        c = 1
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
            except Exception as e:
                print("Run failed. Trying again")

    @staticmethod
    def run(message_2_path, key_string):
        temperatures = [None]
        starting_run = 1
        final_run = 1

        message_1_path = "A:/Projetos A/Plugin-BDD-GPT/src/main/resources/python/message_1_response=user.txt"

        # Cria o arquivo key.txt com a string fornecida
        with open("key.txt", "w") as key_file:
            key_file.write(key_string)
        print("key.txt created with the provided string.")

        for temperature in temperatures:
            for i in range(starting_run, final_run + 1):
                output_folder = f"output_folder/temperature_{temperature}/chat{i}"
                agent = BddAgent()
                os.makedirs(output_folder, exist_ok=True)
                Main.run_like_chat(agent=agent, output_folder=output_folder, temp=temperature,
                                   message_1_path=message_1_path, message_2_path=message_2_path)
                whole_chat_folder = f"{output_folder}/whole_chat"
                os.makedirs(whole_chat_folder, exist_ok=True)
                for c, message in enumerate(agent.messages):
                    Utils.string_to_file(f"{whole_chat_folder}/message_{c + 1}_role={message['role']}.txt",
                                         message["content"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the BddAgent with specified message files.')
    parser.add_argument('message_2_path', type=str, help='Path to the second message file')
    parser.add_argument('key_string', type=str, help='String to write into key.txt')
    args = parser.parse_args()
    print(args)

    Main.run(args.message_2_path, args.key_string)
