from openai import OpenAI
from gpt_input import ChatGptInput


class OpenAiModelHandler:
    def __init__(self, gpt_input: ChatGptInput):
        self.client = OpenAI()
        self.input = gpt_input
        self.completion = None
        self.start_time = None
        self.processing_start_time = None
        self.end_time = None

    def create_prediction(self):
        print("start ai call")
        self.completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": self.input.system_prompt
                },
                {
                    "role": "user",
                    "content": self.input.prompt
                }
            ],
            stream=False
        )
        print("end ai call")



