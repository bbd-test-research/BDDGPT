import time

from openai import OpenAI


class BddAgent:
    def __init__(self):
        self.last_message = None
        self.client = OpenAI()
        self.assistant = self.client.beta.assistants.retrieve(assistant_id='asst_vd1TP6tR9mJJWrYT6JqPt0Si')
        self.thread = None
        self.messages = None

    def initialize_thread(self):
        self.thread = self.client.beta.threads.create()

    def add_message(self, message: str):
        if self.thread is None:
            self.initialize_thread()
        self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message
        )
        self.messages = self.client.beta.threads.messages.list(self.thread.id).data
        self.last_message = self.messages[0]

    def run(self, instructions: str = None):
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            instructions=instructions
        )
        while run.status != "completed":
            # run status cycle guide: https://platform.openai.com/docs/assistants/how-it-works/runs-and-run-steps
            # observation: the code below checks only for the status required in this test. If modifying, check the guide
            # above.
            if run.status == "failed":
                print("Run failed")
                exit(-1)
            if run.status == "cancelled":
                print("Run cancelled")

                exit(-1)
            if run.status in ["expired", "requires_action"]:
                print("Requires action and/or expired")
                exit(-1)

            run = self.client.beta.threads.runs.retrieve(
                run_id=run.id,
                thread_id=self.thread.id)
            time.sleep(0.1)
            messages = self.client.beta.threads.messages.list(thread_id=self.thread.id).data
            self.messages = messages
        self.last_message = self.messages[0]
